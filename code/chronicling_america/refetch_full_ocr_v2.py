"""
GAP 1 FIX v2 — re-fetch FULL OCR, now RATE-LIMIT SAFE.

v1 failed: DELAY=0.5s tripped loc.gov's throttle -> 429 Too Many Requests on
~99% of pages. loc.gov's JSON API allows only a modest request rate. This
version uses a conservative base delay and, on a 429, waits and retries with
exponential backoff instead of recording a permanent error.

Resumable: the 15 pages v1 already saved are kept; this only re-attempts the
rest. Safe to stop (Ctrl-C) and re-run anytime — it picks up where it left off.

Trade-off: at ~8s/page, ~1,335 remaining pages take ~3 hours. Slow, but it's
the only way past the throttle. Leave it running in the background.
"""
import pandas as pd
import requests, time, json
from pathlib import Path

BASE    = Path(r"D:\Shikha\bias_project")
IN_CSV  = BASE / "corpus" / "chronicling_america" / "1920-1922" / "articles.csv"
OUT_CSV = BASE / "corpus" / "chronicling_america" / "1920-1922" / "articles_full_ocr.csv"
ERR_LOG = BASE / "corpus" / "chronicling_america" / "1920-1922" / "ocr_refetch_errors.log"

HEADERS = {"User-Agent": "AcademicResearch/1.0 (gender-bias-panel; mailto:shikhadodecha14@gmail.com)"}
DELAY        = 20.0    # base seconds between pages — conservative for loc.gov
TIMEOUT      = 60
MIN_OK       = 2000   # a real full-OCR page clears this easily
MAX_RETRIES  = 5      # on 429 / transient errors
BACKOFF_BASE = 20     # first 429 wait (s); doubles each retry: 20,40,80,160,320

def _get(url):
    """GET with 429/5xx backoff. Returns response or raises after retries."""
    wait = BACKOFF_BASE
    for attempt in range(MAX_RETRIES):
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        if r.status_code == 200:
            return r
        if r.status_code in (429, 500, 502, 503, 520):
            ra = r.headers.get("Retry-After")
            sleep_s = int(ra) if (ra and ra.isdigit()) else wait
            print(f"      throttled ({r.status_code}); waiting {sleep_s}s "
                  f"(retry {attempt+1}/{MAX_RETRIES})")
            time.sleep(sleep_s)
            wait *= 2
            continue
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

def fetch_full_ocr(item_id):
    meta = get_json(item_id)
    service = meta.get("fulltext_service") or meta.get("resource", {}).get("fulltext_file")
    if not service:
        return None, "no fulltext_service in resource JSON"
    txt = extract_full_text(service)
    if not txt or len(txt) < MIN_OK:
        return None, f"full_text too short ({0 if not txt else len(txt)} chars)"
    return txt, None

def main():
    df = pd.read_csv(IN_CSV)
    print(f"Loaded {len(df)} pages")

    # Resume: keep rows already successfully fetched (text_length >= MIN_OK)
    rows, done_ids = [], set()
    if OUT_CSV.exists():
        prev = pd.read_csv(OUT_CSV)
        good = prev[prev["text_length"] >= MIN_OK]
        rows = good.to_dict("records")
        done_ids = set(good["item_id"])
        print(f"Resuming — {len(done_ids)} pages already have full OCR; "
              f"re-attempting the remaining {len(df) - len(done_ids)}")

    errors = []
    processed = 0
    for _, r in df.iterrows():
        item_id = r["item_id"]
        if item_id in done_ids:
            continue
        processed += 1
        try:
            txt, err = fetch_full_ocr(item_id)
            if err:
                errors.append(f"{item_id}\t{err}")
                txt = ""
            new = dict(r)
            new["text"] = txt
            new["text_length"] = len(txt)
            new["ocr_source"] = "fulltext_service" if txt else "FAILED"
            rows.append(new)
            if txt:
                done_ids.add(item_id)
        except Exception as e:
            errors.append(f"{item_id}\t{type(e).__name__}: {e}")
            new = dict(r); new["text"] = ""; new["text_length"] = 0; new["ocr_source"] = "ERROR"
            rows.append(new)

        if processed % 10 == 0:
            pd.DataFrame(rows).drop_duplicates("item_id", keep="last").to_csv(OUT_CSV, index=False)
            got = sum(1 for x in rows if x.get("text_length", 0) >= MIN_OK)
            print(f"  {processed} attempted | {got} full-OCR ok | {len(errors)} errors this run")
        time.sleep(DELAY)

    out = pd.DataFrame(rows).drop_duplicates("item_id", keep="last")
    out.to_csv(OUT_CSV, index=False)
    if errors:
        ERR_LOG.write_text("\n".join(errors), encoding="utf-8")

    ok = (out["text_length"] >= MIN_OK).sum()
    print(f"\nDone. {len(out)} pages in {OUT_CSV.name}")
    print(f"Full OCR recovered: {ok}/{len(out)}")
    print(f"Mean text_length: {out['text_length'].mean():.0f} (truncated was ~1,060)")
    print(f"Errors this run: {len(errors)}")
    if ok < len(out):
        print("Re-run the script to retry the remaining failures (resumable).")

if __name__ == "__main__":
    main()