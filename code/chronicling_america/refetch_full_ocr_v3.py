"""
GAP 1 FIX v3 — corrects the resume bug in v2.

v2 froze at 300 pages: each run kept the 300 good pages but then re-attempted
the ~24 genuinely-short pages FIRST every time, failing on them and ending the
run before ever reaching the ~1,026 pages it had never tried. Result: stuck.

Root cause was NOT loc.gov throttling — the fetch works fine. It was resume
logic that only skipped GOOD pages, not already-attempted SHORT ones, so it
looped on the same failures.

v3 fix: skip any page already in the output file (good OR short), so every run
advances to genuinely-untried pages. Short pages are recorded once and never
re-attempted. Also lowers MIN_OK to 300 so genuinely-short-but-real pages count
as fetched rather than being retried forever.

Delay kept modest (5s) since there was never a real throttle problem — the 429s
earlier came only from the 0.5s v1 hammering. 5s is safe.
"""
import pandas as pd
import requests, time
from pathlib import Path

BASE    = Path(r"D:\Shikha\bias_project")
IN_CSV  = BASE / "corpus" / "chronicling_america" / "1920-1922" / "articles.csv"
OUT_CSV = BASE / "corpus" / "chronicling_america" / "1920-1922" / "articles_full_ocr.csv"
ERR_LOG = BASE / "corpus" / "chronicling_america" / "1920-1922" / "ocr_refetch_errors.log"

HEADERS = {"User-Agent": "AcademicResearch/1.0 (gender-bias-panel; mailto:shikhadodecha14@gmail.com)"}
DELAY        = 5.0
TIMEOUT      = 60
MIN_KEEP     = 300     # >=300 chars counts as a real (if short) page; recorded, not retried
FULL_OK      = 2000    # >=2000 chars = "full OCR" (for reporting only)
MAX_RETRIES  = 4
BACKOFF_BASE = 15

def _get(url):
    wait = BACKOFF_BASE
    for attempt in range(MAX_RETRIES):
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        if r.status_code == 200:
            return r
        if r.status_code in (429, 500, 502, 503, 520):
            print(f"      transient {r.status_code}; wait {wait}s ({attempt+1}/{MAX_RETRIES})")
            time.sleep(wait); wait *= 2; continue
        r.raise_for_status()
    r.raise_for_status()

def get_json(url):
    if "fo=json" not in url:
        url += ("&" if "?" in url else "?") + "fo=json"
    return _get(url).json()

def extract_full_text(service_url):
    payload = _get(service_url).json()
    for v in payload.values():
        if isinstance(v, dict) and "full_text" in v:
            return v["full_text"]
    return None

def fetch(item_id):
    meta = get_json(item_id)
    service = meta.get("fulltext_service") or meta.get("resource", {}).get("fulltext_file")
    if not service:
        return "", "no fulltext_service"
    txt = extract_full_text(service) or ""
    if len(txt) < MIN_KEEP:
        return txt, f"genuinely short ({len(txt)} chars)"
    return txt, None

def main():
    df = pd.read_csv(IN_CSV)
    print(f"Original corpus: {len(df)} pages")

    # Resume: skip EVERY page already in the output (good OR short) — this is the v2 fix
    rows, done_ids = [], set()
    if OUT_CSV.exists():
        prev = pd.read_csv(OUT_CSV)
        rows = prev.to_dict("records")
        done_ids = set(prev["item_id"])
        good = (prev["text_length"] >= FULL_OK).sum()
        print(f"Already attempted: {len(done_ids)} ({good} full, {len(done_ids)-good} short) — skipping all")
    print(f"Untried pages this run: {len(df) - len(done_ids)}\n")

    errors, processed = [], 0
    for _, r in df.iterrows():
        item_id = r["item_id"]
        if item_id in done_ids:
            continue
        processed += 1
        try:
            txt, note = fetch(item_id)
            if note:
                errors.append(f"{item_id}\t{note}")
            new = dict(r)
            new["text"] = txt
            new["text_length"] = len(txt)
            new["ocr_source"] = "full" if len(txt) >= FULL_OK else ("short" if txt else "empty")
            rows.append(new); done_ids.add(item_id)
        except Exception as e:
            errors.append(f"{item_id}\t{type(e).__name__}: {e}")
            new = dict(r); new["text"]=""; new["text_length"]=0; new["ocr_source"]="ERROR"
            rows.append(new); done_ids.add(item_id)   # record errors too, so we don't loop on them

        if processed % 20 == 0:
            pd.DataFrame(rows).drop_duplicates("item_id", keep="last").to_csv(OUT_CSV, index=False)
            df_now = pd.DataFrame(rows)
            full_now = (df_now["text_length"] >= FULL_OK).sum()
            print(f"  {processed} new attempted | total {len(df_now)} | {full_now} full OCR")
        time.sleep(DELAY)

    out = pd.DataFrame(rows).drop_duplicates("item_id", keep="last")
    out.to_csv(OUT_CSV, index=False)
    if errors:
        ERR_LOG.write_text("\n".join(errors), encoding="utf-8")

    full = (out["text_length"] >= FULL_OK).sum()
    short = ((out["text_length"] >= MIN_KEEP) & (out["text_length"] < FULL_OK)).sum()
    tiny = (out["text_length"] < MIN_KEEP).sum()
    print(f"\nDone. Output now {len(out)}/{len(df)} pages")
    print(f"  full OCR (>=2000): {full}")
    print(f"  short but real (300-2000): {short}")
    print(f"  tiny/empty/error (<300): {tiny}")
    if len(out) < len(df):
        print(f"  {len(df)-len(out)} still untried — re-run to continue (now advances properly).")
    else:
        print("  All pages attempted. Done.")

if __name__ == "__main__":
    main()