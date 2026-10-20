# Congressional Record Extraction Pipeline

## Purpose

Extracts US Congressional floor speeches from GovInfo's API, with speaker-level 
state attribution. Used as a Tier 2 supplementary corpus for the gender bias 
panel — provides convergent validity check against newspaper-derived bias scores.

## Source

- **GovInfo Public API** (https://api.govinfo.gov)
- Collection: **CREC** (Congressional Record, Daily Edition)
- Coverage available: 1994/95 to present (clean XML)
- Coverage available historically (PDF): 1873 onward via CRECB (Bound Edition) — not used in this pipeline

## Current extraction

| Period | Status | Speeches | Words | States |
|---|---|---|---|---|
| January 2024 | Complete | 547 | ~398K | 51 (50 states + DC) |

## Access path

GovInfo's `/published/` and `/collections/CREC/` endpoints proved unreliable 
during testing — both returned 0 results for valid date ranges. The working 
path is the granule-level API:

1. `/packages/{package_id}/summary` — confirms a session day exists
2. `/packages/{package_id}/granules?pageSize=100&offsetMark=*` — lists all 
   speeches/items for that day
3. `/packages/{package_id}/granules/{granule_id}/summary` — provides speaker 
   metadata (member name, state, party, chamber, bioGuideId)
4. `txtLink` from granule summary → fetches HTML-wrapped speech text

**Pagination note:** GovInfo's `nextPage` field returns a full URL, not just 
an offset string. The `call_api` helper detects this and passes the URL 
directly when it starts with `http`.

## Filtering decisions

The extraction filters to **single-speaker HOUSE/SENATE granules only**. 
Reasons:

- **Multi-speaker granules** (e.g., "MORNING-HOUR DEBATE") contain multiple 
  Members speaking — clean state attribution requires text-level parsing, 
  which we defer to a future iteration.
- **Granules with no speaker metadata** are procedural items (votes, motions, 
  prayers, section headers) — not actual speeches.
- **EXTENSIONS** are written remarks entered into record, not delivered on 
  floor — different discourse type.
- **DAILYDIGEST** and **FRONTMATTER** are summaries and metadata.

For January 2024: 1,528 floor granules → 547 single-speaker speeches usable.

## Output format

`corpus/congressional_record/2024-01/speeches.csv` columns:
- `date` — date of the speech (YYYY-MM-DD)
- `package_id` — GovInfo package identifier (CREC-YYYY-MM-DD)
- `granule_id` — GovInfo granule identifier
- `granule_class` — HOUSE or SENATE
- `title` — debate or section title
- `speaker_name` — Member's name (last, first)
- `state` — Member's state (2-letter code)
- `party` — D, R, or I
- `chamber` — H (House) or S (Senate)
- `bioguide_id` — Biographical directory ID (for cross-referencing)
- `speaker_chamber` — Same as chamber for floor speeches
- `text` — Full speech text (HTML stripped via BeautifulSoup)
- `text_length` — Character count of text

## Known limitations

1. **Multi-speaker granules excluded.** ~153 granules in January 2024 had 
   multiple speakers — these contain real speeches but are skipped for clean 
   state attribution. Future work could parse these via Democracy-Lab's 
   speaker_scraper regex approach.

2. **Heavy distribution skew.** Top 5 states (NY, CA, PA, IL, NC) account for 
   41% of January 2024 speeches. Small states (MS, NH, DE, ME) have only 1 
   speech each. State-year cells for small states will need aggregation 
   across time periods for stable embeddings.

3. **Extensions of Remarks not captured.** ~400 EXTENSIONS granules in 
   January 2024 are written remarks entered into record (not delivered on 
   floor). These are technically Member-attributed text but differ in 
   construct from actual speech.

4. **Bound Edition (CRECB, 1873–1994) not yet extracted.** Pre-1995 historical 
   records are PDF-based and require OCR or different parsing. Democracy-Lab's 
   `CRECB_scraper.py` exists for this but is more complex.

5. **API reliability.** GovInfo's API returns intermittent 500 errors, 
   especially on pagination. The `call_api` helper retries with exponential 
   backoff (15s, 30s, 45s).

## Files in this folder

- `README.md` — this file
- `cr_minimal_demo.ipynb` — original proof-of-concept (single speech extraction)
- `cr_january_2024.ipynb` — production extraction for January 2024
- `uscongress-data/` — cloned Democracy-Lab parser (gitignored, not used in this pipeline)

## Dependencies

- `requests` — HTTP client
- `beautifulsoup4` — HTML stripping
- `python-dotenv` — API key loading
- `lxml_html_clean` — required by trafilatura (legacy from earlier exploration)

API key stored in `.env` at project root as `GOVINFO_API_KEY`.

## Next steps

1. Scale extraction to additional months (Feb 2024, Mar 2024, ...)
2. Recover multi-speaker granules via text-level speaker parsing
3. Decide whether to extend to pre-1995 historical data via CRECB
4. Train embeddings per state-year, compute bias scores, compare against 
   newspaper-derived measures (convergent validity check)