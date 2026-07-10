"""
Extract Chronicling America demo slices for 1940 and 1960 — FULL OCR from the start.

Adds two historical time points to the demo (previously only 1920-22).
Same 9 states, 50 pages per (state, year). Fetches full OCR via the
fulltext_service endpoint (the fix proven in refetch_full_ocr_v3), so no
truncation to fix later. Output matches articles_full_ocr.csv structure, so
the embedding notebooks read it with no changes.

Resilient: retries on transient errors, resumable (skips pages already saved),
polite delay to avoid loc.gov throttling. Run in the project venv.
"""
import requests, time, re
import pandas as pd
from pathlib import Path

BASE = Path(r"D:\Shikha\bias_project")
OUT_DIR = BASE / "corpus" / "chronicling_america"
HEADERS = {"User-Agent": "AcademicResearch/1.0 (gender-bias-panel; mailto:shikhadodecha14@gmail.com)"}

STATES = {
    "OH": "ohio", "WY": "wyoming", "CA": "california", "TX": "texas",
    "IL": "illinois", "MS": "mississippi", "MT": "montana",
    "OR": "oregon", "NY": "new york",
}
YEARS = [1940, 1960]
PAGES_PER_CELL = 50
SEARCH_DELAY = 6.0
FETCH_DELAY  = 10.0    # full-OCR fetches — keep slow to avoid throttle
TIMEOUT = 60
MIN_OK = 2000
MAX_RETRIES = 3
BACKOFF = 15

def _get(url, params=None):
    wait = BACKOFF
    for attempt in range(MAX_RETRIES):
        try:
            r = requests.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)
            if r.status_code == 200:
                _ = r.content   # force full download here so IncompleteRead surfaces now
                return r
            if r.status_code in (429, 500, 502, 503, 520):
                print(f"      transient {r.status_code}; wait {wait}s")
                time.sleep(wait); wait *= 2; continue
            return None
        except Exception as e:
            print(f"      connection error ({type(e).__name__}); retry {attempt+1}/{MAX_RETRIES}")
            time.sleep(wait); wait *= 2; continue
    return None

def list_page_urls(state_name, year, want):
    """Get up to `want` page resource URLs for a state-year."""
    urls = []
    page = 1
    while len(urls) < want:
        r = _get("https://www.loc.gov/collections/chronicling-america/",
                 params={"q": state_name, "dates": f"{year}/{year}",
                         "dl": "page", "fo": "json", "c": 25, "sp": page})
        if r is None:
            break
        results = r.json().get("results", [])
        if not results:
            break
        for item in results:
            u = item.get("id") or item.get("url")
            if u and "/resource/" in u:
                urls.append(u if u.startswith("http") else "https://www.loc.gov" + u)
        page += 1
        time.sleep(SEARCH_DELAY)
        if page > 10:
            break
    return urls[:want]

def fetch_full_ocr(item_id):
    meta_url = item_id + ("&" if "?" in item_id else "?") + "fo=json"
    r = _get(meta_url)
    if r is None:
        return None
    meta = r.json()
    service = meta.get("fulltext_service") or meta.get("resource", {}).get("fulltext_file")
    if not service:
        return None
    rr = _get(service)
    if rr is None:
        return None
    for v in rr.json().values():
        if isinstance(v, dict) and "full_text" in v:
            return v["full_text"]
    return None

def parse_meta(item_id):
    m = re.search(r"/resource/([^/]+)/(\d{4}-\d{2}-\d{2})/ed-(\d+)/", item_id)
    sp = re.search(r"[?&]sp=(\d+)", item_id)
    lccn = m.group(1) if m else ""
    date = m.group(2) if m else ""
    return lccn, date

def main():
    for year in YEARS:
        out_csv = OUT_DIR / f"articles_{year}.csv"
        rows, done = [], set()
        if out_csv.exists():
            prev = pd.read_csv(out_csv)
            rows = prev.to_dict("records"); done = set(prev["item_id"])
            print(f"[{year}] resuming — {len(done)} pages already saved")

        for abbr, name in STATES.items():
            have = sum(1 for r in rows if r.get("state_abbr") == abbr)
            if have >= PAGES_PER_CELL:
                continue
            print(f"[{year}] {abbr} ({name}) — listing pages...")
            urls = list_page_urls(name, year, PAGES_PER_CELL * 2)  # over-list; some fail
            got = have
            for u in urls:
                if got >= PAGES_PER_CELL:
                    break
                if u in done:
                    continue
                txt = fetch_full_ocr(u)
                time.sleep(FETCH_DELAY)
                if not txt or len(txt) < MIN_OK:
                    continue
                lccn, date = parse_meta(u)
                rows.append({"state": name, "state_abbr": abbr, "year": year,
                             "item_id": u, "date": date, "text_length": len(txt),
                             "text": txt})
                done.add(u); got += 1
                if got % 10 == 0:
                    pd.DataFrame(rows).drop_duplicates("item_id").to_csv(out_csv, index=False)
                    print(f"      {abbr}: {got}/{PAGES_PER_CELL}")
            pd.DataFrame(rows).drop_duplicates("item_id").to_csv(out_csv, index=False)
            print(f"[{year}] {abbr}: {got} pages saved")

        final = pd.DataFrame(rows).drop_duplicates("item_id")
        final.to_csv(out_csv, index=False)
        print(f"[{year}] DONE — {len(final)} pages, mean {int(final['text_length'].mean())} chars -> {out_csv.name}\n")

if __name__ == "__main__":
    main()