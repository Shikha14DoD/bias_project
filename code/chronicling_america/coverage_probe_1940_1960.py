"""
Coverage probe — how many Chronicling America pages exist per state for
candidate demo years (1940, 1960), before committing to extraction.

Queries loc.gov the same way the existing extraction does. Reports page
counts per (state, year) so we only extract years/states with usable
coverage. No extraction — just counts. Run in the project venv.
"""
import requests, time

HEADERS = {"User-Agent": "AcademicResearch/1.0 (gender-bias-panel; mailto:shikhadodecha14@gmail.com)"}

STATES = {
    "OH": "ohio", "WY": "wyoming", "CA": "california", "TX": "texas",
    "IL": "illinois", "MS": "mississippi", "MT": "montana",
    "OR": "oregon", "NY": "new york",
}
BASELINE_YEAR = 1921   # known-good sanity check

def count_pages(state_name, year):
    url = "https://www.loc.gov/collections/chronicling-america/"
    params = {"q": state_name, "dates": f"{year}/{year}", "dl": "page",
              "fo": "json", "c": 1}
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=30)
        if r.status_code != 200:
            return None
        data = r.json()
        total = data.get("pagination", {}).get("of")
        if total is None:
            total = data.get("search", {}).get("hits")
        return total
    except Exception as e:
        return None

print(f"{'State':<14} {'1921(base)':>11} {'1940':>8} {'1960':>8}")
print("-" * 45)
for abbr, name in STATES.items():
    base = count_pages(name, BASELINE_YEAR); time.sleep(1.5)
    y40  = count_pages(name, 1940);          time.sleep(1.5)
    y60  = count_pages(name, 1960);          time.sleep(1.5)
    fmt = lambda v: f"{v:,}" if isinstance(v, int) else str(v)
    print(f"{name:<14} {fmt(base):>11} {fmt(y40):>8} {fmt(y60):>8}")

print("\nReading:")
print("- 1921 = sanity baseline (known to work).")
print("- 1940/1960 with hundreds+ per state -> viable to extract.")
print("- near 0 -> little/no coverage; skip that year or pick another.")