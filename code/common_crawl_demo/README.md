# Common Crawl Demo

## Purpose

Exploratory script to evaluate Common Crawl / CC-News as a potential 
corpus source for the modern (2015–present) period of the bias panel.

## Goals

1. Confirm whether Common Crawl indexes US newspaper domains we care about
2. Check coverage density across small/medium/large state newspapers
3. Assess text extraction quality (article content vs. boilerplate/ads/paywall stubs)
4. Decide whether Common Crawl is a viable free fallback if NewsBank / 
   ProQuest U.S. Newsstream access isn't available

## Status

Exploratory — not part of the production pipeline.

## Files

- `cc_test.ipynb` — main demo notebook
- `README.md` — this file

## Dependencies

Python packages (installed in project venv):
- `cdx_toolkit` — query Common Crawl index
- `warcio` — parse WARC files
- `trafilatura` — extract clean article text from HTML
- `requests` — HTTP fetching

## Decision criteria

Common Crawl is viable for this project if:
- [ ] At least one major newspaper from each target state is indexed
- [ ] Articles per paper per month is reasonable (>50 for medium states)
- [ ] Text extraction returns clean article body, not navigation/ads/paywall stubs
- [ ] Coverage holds up across 2015–present (not just recent years)

## Findings

(To be filled in after running the demo. Log decisions in 
`notes/compilation_log.md` as well.)

## Related

- Project root: `D:\Shikha\bias_project`
- Main log: `notes/compilation_log.md`