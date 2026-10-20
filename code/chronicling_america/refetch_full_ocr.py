"""
GAP 1 FIX — re-fetch FULL OCR for the Chronicling America 1920-1922 corpus.

The original articles.csv 'text' column holds the loc.gov search 'description'
field, hard-truncated to ~1,100 chars (max 1,471 across all 1,350 pages).
A real page is ~15,000-25,000 chars. This rebuilds the text column from the
full OCR via the page resource JSON's 'fulltext_service' endpoint
(host: tile.loc.gov, which is NOT the Cloudflare-blocked chroniclingamerica host).

Reuses the item_id URLs already in articles.csv — no re-running the search.
Writes a NEW file (articles_full_ocr.csv); the original is left untouched so
you can diff / fall back.

Run in the project venv. Polite ~2 req/sec; ~1,350 pages -> roughly 25-45 min.
Resumable: re-running skips rows already done in the output file.
"""
import pandas as pd
import requests, time, json
from pathlib import Path

BASE    = Path(r"D:\Shikha\bias_project")
IN_CSV  = BASE / "corpus" / "chronicling_america" / "1920-1922" / "articles.csv"
OUT_CSV = BASE / "corpus" / "chronicling_america" / "1920-1922" / "articles_full_ocr.csv"
ERR_LOG = BASE / "corpus" / "chronicling_america" / "1920-1922" / "ocr_refetch_errors.log"

HEADERS = {"User-Agent": "AcademicResearch/1.0 (gender-bias-panel; mailto:shikhadodecha14@gmail.com)"}
DELAY   = 0.5     # seconds between pages; loc.gov tolerates ~2-4 req/sec
TIMEOUT = 60
MIN_OK  = 2000    # a successful full-OCR fetch should clear this many chars

def get_json(url):
    if "fo=json" not in url:
        url += ("&" if "?" in url else "?") + "fo=json"
    r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()

def extract_full_text(service_url):
    """Fetch the fulltext_service URL and pull the 'full_text' value out of
    its JSON wrapper. The wrapper is keyed by an internal segment path, so we
    take the first value rather than reconstruct the key."""
    r = requests.get(service_url, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    payload = r.json()
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
    print(f"Loaded {len(df)} pages from {IN_CSV.name}")

    # Resume support: keep rows already fetched
    done_ids = set()
    if OUT_CSV.exists():
        prev = pd.read_csv(OUT_CSV)
        done_ids = set(prev["item_id"])
        print(f"Resuming — {len(done_ids)} pages already done")
        rows = prev.to_dict("records")
    else:
        rows = []

    errors = []
    for i, r in df.iterrows():
        item_id = r["item_id"]
        if item_id in done_ids:
            continue
        try:
            txt, err = fetch_full_ocr(item_id)
            if err:
                errors.append(f"{item_id}\t{err}")
                txt = ""   # keep the row, empty text, so it's visible as a miss
            new = dict(r)
            new["text"] = txt
            new["text_length"] = len(txt)
            new["ocr_source"] = "fulltext_service" if txt else "FAILED"
            rows.append(new)
        except Exception as e:
            errors.append(f"{item_id}\t{type(e).__name__}: {e}")
            new = dict(r); new["text"] = ""; new["text_length"] = 0; new["ocr_source"] = "ERROR"
            rows.append(new)

        if (i + 1) % 25 == 0:
            pd.DataFrame(rows).to_csv(OUT_CSV, index=False)   # checkpoint
            got = sum(1 for x in rows if x.get("text_length", 0) >= MIN_OK)
            print(f"  {i+1}/{len(df)} processed | {got} full-OCR ok | {len(errors)} errors")
        time.sleep(DELAY)

    out = pd.DataFrame(rows)
    out.to_csv(OUT_CSV, index=False)
    if errors:
        ERR_LOG.write_text("\n".join(errors), encoding="utf-8")

    ok = (out["text_length"] >= MIN_OK).sum()
    print(f"\nDone. {len(out)} pages written to {OUT_CSV.name}")
    print(f"Full OCR recovered: {ok}/{len(out)}")
    print(f"Mean text_length now: {out['text_length'].mean():.0f} (was ~1,060)")
    print(f"Errors logged: {len(errors)} -> {ERR_LOG.name if errors else '(none)'}")
    print("\nNext: point the four embedding notebooks at articles_full_ocr.csv and re-run the hist_1920s cells.")

if __name__ == "__main__":
    main()