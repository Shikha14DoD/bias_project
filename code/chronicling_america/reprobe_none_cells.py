"""
Re-probe the three (state, year) cells that returned None in the coverage probe,
to confirm whether they're query hiccups (expected) or genuinely no coverage.
Retries each a few times and also tries the alt count field.
"""
import requests, time

HEADERS = {"User-Agent": "AcademicResearch/1.0 (gender-bias-panel; mailto:shikhadodecha14@gmail.com)"}

CELLS = [("ohio", 1960), ("california", 1921), ("mississippi", 1940)]

def count_pages(state_name, year, tries=3):
    url = "https://www.loc.gov/collections/chronicling-america/"
    params = {"q": state_name, "dates": f"{year}/{year}", "dl": "page",
              "fo": "json", "c": 1}
    for attempt in range(tries):
        try:
            r = requests.get(url, params=params, headers=HEADERS, timeout=40)
            if r.status_code == 200:
                data = r.json()
                total = (data.get("pagination", {}).get("of")
                         or data.get("search", {}).get("hits")
                         or data.get("pagination", {}).get("total"))
                if total is not None:
                    return total
            time.sleep(4)   # wait and retry — likely a transient empty response
        except Exception as e:
            time.sleep(4)
    return None

print(f"{'State':<14} {'Year':>6} {'Pages':>12}")
print("-" * 34)
for name, year in CELLS:
    n = count_pages(name, year)
    time.sleep(2)
    val = f"{n:,}" if isinstance(n, int) else "still None"
    print(f"{name:<14} {year:>6} {val:>12}")

print("\n- real number -> was a query hiccup; state-year IS viable.")
print("- still None after retries -> genuinely no/low coverage; handle that cell.")