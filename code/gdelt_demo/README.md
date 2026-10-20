# GDELT Article Text Extraction Pipeline

## Purpose

Extracts article text from GDELT 2.0 Global Knowledge Graph URLs for use
as a modern corpus (2015–present) in the gender bias state-year panel.

## Source

- **GDELT 2.0 GKG** via Google BigQuery
- Table: `gdelt-bq.gdeltv2.gkg_partitioned`
- Google Cloud project: `bias-project-gdelt` (Sandbox mode, no billing)
- Coverage: 2015–present

## Current extraction

| Period | URLs sampled | Successful | Failed | Success rate |
|---|---|---|---|---|
| January 2024 | 1,530 | ~690 | 828 | ~45% |

## Pipeline architecture

1. **BigQuery query** → article URLs + metadata (CSV)
   - 30 URLs sampled per state × 51 states = 1,530 total
   - Filtered to US sources via source-domain → state mapping

2. **Article text fetching** (`gdelt_extraction.ipynb`)
   - Uses `trafilatura` for clean text extraction
   - Realistic Chrome browser user-agent to reduce blocking
   - 1.5s polite delay between requests
   - Resume support — skips already-processed URLs on restart
   - 5 outcome categories: success / paywall / no_text / fetch_failed / error

3. **Output** → `corpus/gdelt/2024-01/gdelt_articles_with_text.csv`

## Known limitations

- **GDELT provides URLs, not article text.** Text must be fetched separately
  from publisher websites — this is the main engineering risk.
- **~54% failure rate** in January 2024 sample due to bot blocking, 403
  errors, and timeouts. This is worse than the 60-80% projected range.
- **No paywalled content** — paywalled articles return hard blocks, not
  stub pages, so they appear as failures rather than paywall stubs.
- **State attribution** relies on source-domain → state mapping, which
  requires manual curation and introduces some error.

## Key files

| File | Description |
|---|---|
| `code/gdelt_demo/gdelt_extraction.ipynb` | BigQuery query + fetch pipeline |
| `corpus/gdelt/2024-01/gdelt_articles_with_text.csv` | Extracted article text |
| `corpus/gdelt/2024-01/fetch_errors.log` | Failed URLs with error types |

## Access requirements

- Google account with BigQuery Sandbox access
- No API key required for GDELT public dataset
- No billing required (Sandbox mode, within free tier)