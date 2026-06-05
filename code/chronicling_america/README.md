# Chronicling America Extraction Pipeline

## Purpose

Extracts historical newspaper OCR text from the Library of Congress
Chronicling America collection. Used as the historical corpus (1900–1963)
for the gender bias state-year panel.

## Source

- **loc.gov API** (https://www.loc.gov/collections/chronicling-america/)
- Coverage: 1700s–1963 (strongest 1900–1922)
- No API key required
- Rate limit: polite 1s delay recommended

## Current extraction

| Period | States | Pages fetched | Notes |
|---|---|---|---|
| 1920–1922 | 9 (OH WY CA TX IL MS MT OR NY) | 1,350 | Demo slice |

## Key technical notes

- Legacy `chroniclingamerica.loc.gov` API is **dead** — returns 403
  Cloudflare block. Do not use.
- Use new `loc.gov` API with `dl=page` parameter to get page-level results
- OCR text is in the `description` field of each result — no separate fetch
- Multi-word state names need spaces: `'new york'` not `'new-york'`
- Date filter: use `start_date=YYYY-01-01` and `end_date=YYYY-12-31`

## Pipeline

1. Coverage check — query page counts per state-year before downloading
2. Page fetch — query loc.gov API with state + date + `dl=page` filters
3. Text extraction — pull `description` field from each result
4. Save to CSV with state, year, date, title, text

## Key files

| File | Description |
|---|---|
| `code/chronicling_america/chron_am_1920_1922.ipynb` | Extraction notebook |
| `corpus/chronicling_america/1920-1922/articles.csv` | Extracted OCR text |
| `corpus/chronicling_america/1920-1922/errors.log` | Pages with no text |