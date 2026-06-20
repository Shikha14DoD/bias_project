For each task: date, what I did, what worked, what didn't, what I learned.

branch-> "gender_bias_in_usa"

## 2026-05-09 — GSS validation data downloaded

**Source:** gssdataexplorer.norc.org (Extracts tool)  
**Variables (19):** YEAR, ID_, BALLOT, FEFAM, FEPRES, FEWORK, FECHLD, FEHIRE, FEHELP, FEPOL, AGE, SEX, RACE, EDUC, MARITAL, REG16, REGION, REGION_7222, REG16_7222  
**Years:** 1972–2024 (all available)  
**Rows:** 75,699 respondents (verified — line count of .dat file and Excel data sheet both confirm)  
**Saved to:** `validation_data/gss/`
- `gss_gender_attitudes.xlsx`
- `gss_gender_attitudes.dat`
- `gss_gender_attitudes.do`
- `post_processing_output.json`

**Excel file structure (3 sheets):**
- **Data:** 75,699 rows × 19 columns of respondent-level data (one row per person interviewed)
- **Variables:** codebook listing each variable's name, short label, and original survey question text
- **Codes:** codebook mapping numeric codes to their meanings, including missing-data flags

**Important — missing-data handling:** GSS uses negative integer codes for missing data, applied uniformly across variables. Examples observed in the Codes sheet:
- -100 = Inapplicable
- -99 = No answer
- -98 = Do not Know / Cannot Choose
- -97 = Skipped on Web
- -95 = Uncodable
- -90 = Refused
- -70 = Not available in this year (question not asked)

These negative values must be filtered out (treated as NA) before any statistical computation. Naive means/correlations including negative codes will be wildly wrong.

**Notes:**
- All 75,699 respondents retained — no row-level filtering applied. Every GSS respondent 1972–2024 is in the file regardless of whether they answered the gender questions. Per-question missing-value filtering will happen during analysis (drop rows with negative codes for the specific variable being analyzed).
- BALLOT included to distinguish "not asked" (different ballots ask different questions) from "didn't answer."
- **GSS public-use file does NOT include state identifiers** (only REGION). Validation strategy:
  - Primary: aggregate bias scores to Census regions and validate at region-year level using REGION_7222 (9-category).
  - Secondary: use MRP (multilevel regression and post-stratification) with demographics + REGION to estimate state-level attitudes.
- Geographic variables: both new 4-category (REGION, REG16) and original 9-category (REGION_7222, REG16_7222) codings included. The 9-category versions are preferred for finer geographic resolution and to align with Garg et al. 2018.
- Stata format delivered as .dat (raw data) + .do (Stata script). Run the .do in Stata to produce a labeled .dta file. Excel works directly for inspection without Stata.
- Variables and Codes are stored as reference sheets in the Excel file; not merged into Data. Workflow is to load Data, reference Codes for missing-data filtering, reference Variables for documentation.

## 2026-05-09 — Caliskan 2017 word lists pulled

Word lists pulled from : Semantics derived automatically from language corpora contain human-like biases | https://www.science.org/doi/10.1126/science.aal4230

**Source:** Caliskan, A., Bryson, J. J., & Narayanan, A. (2017). "Semantics derived automatically from language corpora contain human-like biases." *Science* 356(6334), 183–186. https://www.science.org/doi/10.1126/science.aal4230

Word lists transcribed directly from the supplementary materials PDF, saved alongside the derived lists in `word_lists/caliskan_2017/`.

**Files saved (15 total):**

*WEAT 6 — Career-Family bias (4 files):*
- `male_names_weat6.txt`, `female_names_weat6.txt` — 8 European-American names each
- `career_terms_weat6.txt`, `family_terms_weat6.txt` — 8 terms each

*WEAT 7 — Math-Arts bias (4 files):*
- `math_terms_weat7.txt`, `arts_terms_weat7.txt` — 8 terms each
- `male_terms_weat7.txt`, `female_terms_weat7.txt` — 8 generic gender terms each

*WEAT 8 — Science-Arts bias (4 files):*
- `science_terms_weat8.txt`, `arts_terms_weat8.txt` — 8 terms each
- `male_terms_weat8.txt`, `female_terms_weat8.txt` — 8 kinship-focused gender terms each

*WEFAT 1 — Occupation associations (3 files):*
- `occupations_wefat1.txt` — 50 occupations matched to Bureau of Labor Statistics categories
- `male_terms_wefat1.txt`, `female_terms_wefat1.txt` — 8 gender terms each (identical content to WEAT 7 lists)

**Notes:**
- All lists transcribed directly from Caliskan et al. 2017 supplementary materials PDF (saved in same folder).
- **WEAT 7 and WEAT 8 deliberately use different male/female term sets** — WEAT 7 uses generic terms (male, man, boy, brother, ...) replicating Nosek et al. 2002a; WEAT 8 uses kinship terms (brother, father, uncle, grandfather, ...) replicating Nosek et al. 2002b. Kept separate per the original paper's methodology.
- **WEFAT 1's male and female attribute lists are identical to WEAT 7's lists** (both cite Nosek et al. 2002, source (9) in Caliskan 2017). Saved as separate files (`male_terms_wefat1.txt`, `female_terms_wefat1.txt`) for code clarity and explicit per-test file structure, even though contents are identical to WEAT 7.
- **WEAT 6 uses names** (John, Paul, Amy, Joan, ...) rather than generic terms, anchoring the test in person-referential text and avoiding polysemy issues with generic gender terms.
- **WEFAT 1 is the test Garg et al. 2018 validates against Bureau of Labor Statistics occupation gender composition data** — strongest construct validity for our state-year panel.
- WEAT 1, 2, 3, 4, 5, 9, 10 not pulled — out of scope (race bias, age bias, flowers/insects, etc. are not relevant for the gender-focused state-year panel).

**Mapping to project bias measures:**
- *Career-family bias* (proposal Measure 1) ← WEAT 6 files
- *Competence-warmth bias* (proposal Measure 2) ← will need to source separately, not in Caliskan 2017
- *Leadership-subordination bias* (proposal Measure 3) ← will need to source separately, not in Caliskan 2017
- *Occupation associations* (proposal Measure 4) ← WEFAT 1 files (used by Garg 2018 for Census validation)

WEAT 7 and WEAT 8 (math-arts, science-arts) are useful supplementary measures of gender-stereotyped academic-domain associations but don't directly map to the four core measures in our proposal. Including them adds breadth and lets us replicate Caliskan's original results on our state-year embeddings as a methodological sanity check.

## 2026-05-10 — Garg 2018 materials pulled

**Source:** Garg, N., Schiebinger, L., Jurafsky, D., & Zou, J. (2018). "Word embeddings quantify 100 years of gender and ethnic stereotypes." *PNAS* 115(16), E3635–E3644. https://doi.org/10.1073/pnas.1720347115

**GitHub repo:** https://github.com/nikhgarg/EmbeddingDynamicStereotypes  
**Cloned to:** `code/garg_reference/` (gitignored — not committed to our repo)

**Files copied to `word_lists/garg_2018/` (15 total):**

*Gender axis stimuli:*
- `male_pairs.txt`, `female_pairs.txt` — paired gender terms used to define the gender direction in embedding space

*Occupation lists and validation data:*
- `occupations1950.txt` — full occupation list keyed to 1950 Census codes
- `occupations1950_professional.txt` — subset of professional occupations
- `occupation_map.csv` — mapping between occupation names and Census codes
- `occupation_percentages_gender_occ1950.csv` — historical female/male composition of each occupation by Census year (1880–2015 range, national-level)

*Adjective category lists:*
- `adjectives_appearance.txt` — looks-related descriptors
- `adjectives_intelligencegeneral.txt` — mental capability descriptors
- `adjectives_sensitive.txt` — emotional/sensitivity descriptors
- `adjectives_otherization.txt` — foreign/outsider framing descriptors
- `adjectives_princeton.txt` — adjectives from Princeton Trilogy stereotyping studies
- `adjectives_williamsbest.txt` — Williams & Best cross-cultural stereotype adjectives

*Personality and stereotype reference data:*
- `personalitytraits_original.txt` — Big Five-style personality traits
- `mturk_stereotypes.csv` — crowdsourced gender stereotype ratings
- `princeton_stereotypes.csv` — Princeton stereotype ratings

**Notes on `occupation_percentages_gender_occ1950.csv` specifically:**
- Columns: Census year, Occupation, Total Weight (count of workers), Female (fraction), Male (fraction)
- Data is Census-derived — Garg et al. processed raw Census records (likely via IPUMS using the standardized OCC1950 occupation classification, which provides cross-time consistency).
- **National-level only** — no state breakdown. Useful as a template for what occupation-gender validation data looks like, but for our state-year project, we will need to pull fresh IPUMS data at state-level resolution.
- Visible year range in inspection: 1880–2015.
- Sanity check: occupational gender patterns visible in the data align with documented history (e.g., 1950 guards 2% female, 1940 photographers 8.8% female, 2007 dancers 79% female).

**Files NOT copied (out of scope for gender-focused project):**
- Race-related: `names_asian.txt`, `names_black.txt`, `names_chinese.txt`, `names_hispanic.txt`, `names_russian.txt`, `names_white.txt`, `occupation_percentages_race_occ1950.csv`
- Religion-related: `words_christianity.txt`, `words_islam.txt`, `words_terrorism.txt`
- Internal computation artifacts: `vocab_counts/` (corpus-specific token counts)
- Duplicate format: `adjectives_williamsbest.csv` (kept .txt version only)

**Mapping to our project bias measures:**
- *Career-family bias* (Measure 1) ← Caliskan WEAT 6 (already pulled)
- *Competence-warmth bias* (Measure 2) ← Garg `adjectives_intelligencegeneral.txt` + `adjectives_sensitive.txt`
- *Leadership-subordination bias* (Measure 3) ← will need additional curation; Garg's adjective lists provide some terms but not a clean leadership/subordination split
- *Occupation associations* (Measure 4) ← Garg `occupations1950.txt` + `occupation_percentages_gender_occ1950.csv` (national reference) → will supplement with state-level IPUMS pulls

**Reference scripts in `code/garg_reference/` (gitignored — for reference only):**
- `dataset_utilities/create_yrly_datasets.py` — per-year corpus preprocessing
- `dataset_utilities/pipeline.py` — embedding training and bias-measure pipeline
- `changes_over_time.py` — main analysis script for temporal bias trends
- Will refer to these when writing our own embedding training and bias computation code; not directly reused.

## 2026-05-15 — GDELT setup, pipeline architecture, and corpus scope finding

### GDELT BigQuery access set up

**Why this approach:** GDELT 2.0's Global Knowledge Graph (GKG) is the primary 
modern-era source for news article metadata. Three access methods are available 
(raw CSV downloads, DOC API, BigQuery), with BigQuery being the right choice 
for our project's scale:
- Raw CSV downloads — impractical (hundreds of GB of 15-minute files since 2015)
- DOC API — query result limits cap useful pulls at a few hundred records
- BigQuery — handles millions of records per query via SQL, free tier 
  (1 TB/month query processing) sufficient for anticipated workload

**Setup completed:**
- Google Cloud project created: `bias-project-gdelt` (Project ID: bias-project-gdelt)
- Working in BigQuery Sandbox mode (no billing required, 1 TB/month free queries)
- Verified access to public dataset `gdelt-bq.gdeltv2.gkg_partitioned`
- Browsed full schema via Explorer panel to confirm column names

**Test queries run:**
1. Single-day count for 2020-01-01: returned 250,556 GKG records, confirming 
   read access and dataset volume
2. (Optional follow-up: single-source pull for azcentral.com to verify schema 
   matches documentation)

### Key GKG fields for our project
Verified in BigQuery schema view:
- `DATE` — publication timestamp at 15-minute granularity
- `SourceCommonName` — source domain (e.g., azcentral.com) for state mapping
- `DocumentIdentifier` — full article URL (used for text fetching downstream)
- `V2Themes` — GDELT's theme taxonomy, semicolon-separated
- `V2Tone` — comma-separated tone scores (positive%, negative%, polarity, 
  activity, etc.)
- `V2Locations` — geocoded locations mentioned in article
- `SourceCollectionIdentifier` — distinguishes news media from other sources

Authoritative reference: GDELT GKG 2.1 Codebook at 
http://data.gdeltproject.org/documentation/GDELT-Global_Knowledge_Graph_Codebook-V2.1.pdf

### Cost management approach
- Always filter on `_PARTITIONTIME` in WHERE clause to limit partition scanning
- Use `gkg_partitioned` table (not `gkg`) for cheaper date-filtered queries
- A typical single-day, single-source query processes < 1 GB (well within free tier)
- Without partition filtering, queries can scan hundreds of GB

### Pipeline architecture (modern coverage, if confirmed in scope)

End-to-end pipeline:
1. BigQuery query → article URLs + metadata (CSV export)
2. Article text fetcher → raw article text from publisher URLs
3. Text cleaning + concatenation → per (state, year) corpus files
4. Word embedding training → per-cell embeddings
5. WEAT bias computation using Caliskan/Garg word lists → bias scores
6. Aggregate into state-year panel CSV
7. Validation against GSS, Census occupation data, CAWP

### Key engineering risk: article-text-fetching
GDELT provides URLs and metadata, NOT full article text. Stage 2 of the 
pipeline requires fetching article text from publisher URLs, which involves:
- Anti-bot detection on news sites
- Paywalls (concentrated in major outlets and recent years)
- URL rot for older articles
- Boilerplate extraction (navigation, ads, comments)
- Per-site rate limits and terms of service

**Realistic fetch success rate:** Likely 60–80% depending on source mix and 
time period. Concentration of paywalls at higher-quality outlets introduces 
sampling concerns about what the corpus actually represents.

**Mitigation plan:** Before committing to GDELT-only modern coverage, run a 
small fetch experiment (~200 URLs from one month, mixed sources) to measure 
realistic success rate. If success rate is low, NewsBank access becomes more 
critical for the modern panel.

### Storage estimates
Rough projections for full modern panel (50 states × 10 years):
- BigQuery URL CSVs: ~5 GB
- Raw fetched text: ~250 GB
- Cleaned per-cell corpora: ~100 GB
- Trained embeddings: ~25 GB
- Final bias scores: a few MB

Manageable on local machine with external storage or Google Cloud Storage.

### Other modern-corpus access methods evaluated
- GDELT Summary site (summary.gdeltproject.org): currently has expired SSL 
  certificate (NET::ERR_CERT_DATE_INVALID). Worked around by using DOC API 
  on properly-secured api.gdeltproject.org domain for any future exploration.
- Google Cloud Marketplace listings for GDELT: show "GDELT 2.0 Event Database" 
  but this is the wrong table for our project (we need GKG, not Events). 
  Adding via Marketplace is unnecessary since public datasets are directly 
  queryable in BigQuery.

### Outstanding scope question (sent to manager)
Awaiting manager's response on target year range:
- Historical only (1900–1922 strong, 1923–1963 thin)
- Modern only (1985–2014 via NewsBank if access granted, 2015+ via GDELT)
- Full span with the 1923–1984 gap documented

GDELT setup is complete and ready to use immediately once modern coverage 
is confirmed in scope. No further GDELT work planned until scope clarified, 
to avoid building infrastructure for a date range that may not be targeted.

### Sources not yet explored (deferred until scope confirmed)
For potential 1964–1984 gap filling if full historical arc is in scope:
- HathiTrust digital library (state-of-publication metadata available)
- Congressional Record (state-tagged via representatives)
- State-of-the-state addresses (one per state per year)
- Internet Archive newspaper digitization
- Common Crawl filtered to US news domains (heavy engineering required)


## 2026-05-29 — Common Crawl evaluation, NJIT ProQuest access discovery, TDM Studio trial requested

### Common Crawl exploration (later determined redundant)

**Context:** Started this thread under the assumption that NewsBank access wouldn't 
materialize, leaving a corpus gap for 1985+. Explored Common Crawl as a potential 
free fallback for the modern period.

**Setup completed:**
- Created `code/common_crawl_demo/` folder with `cc_test.ipynb` and `README.md`
- Set up Python virtual environment at project root (`venv/`)
- Installed packages: `cdx_toolkit`, `warcio`, `trafilatura`, `lxml_html_clean`, 
  `requests`
- Selected venv as VS Code Python interpreter for the notebook

**Demo attempt:**
- Targeted 11 US newspaper domains across 9 states (large/medium/small mix)
- Queried Common Crawl CDX index for 2024 coverage

**Result:** Free HTTP CDX endpoint (`index.commoncrawl.org`) was unreliable — 
connections dropped on every query, both through `cdx_toolkit` and via direct 
HTTP. Confirmed it's a server-side issue, not our code. Production access would 
require AWS Athena (paid) or direct WARC file processing (engineering-heavy).

**Realized mid-thread:** Common Crawl would have covered 2015–present, which is 
the same period GDELT BigQuery (already set up on 2026-05-15) covers. So the 
exploration was largely redundant — GDELT already addresses this window. 
Should have checked existing project state before adding a new corpus source.

**Decision:** Paused Common Crawl. Keeping the notebook/venv setup in case 
relevant later, but not pursuing further. GDELT remains the 2015–present 
solution.

### NJIT ProQuest access confirmed

**Discovery:** Logged into ProQuest via NJIT and confirmed access to 7 databases, 
including the full U.S. Newsstream family:
- U.S. Newsstream Collection (1980–current)
- U.S. Major Dailies (1980–current)
- U.S. Hispanic Newsstream (Spanish + English Hispanic press)
- U.S. Midwest Newsstream
- U.S. North Central Newsstream
- U.S. Northeast Newsstream
- U.S. South Central Newsstream
- U.S. Southeast Newsstream
- U.S. West Newsstream
- CBS News 60 Minutes (1997–2014) — TV transcripts

**Content verified:** Opened sample article (Minneapolis Star and Tribune, 
Jan 3 1986) — full-text narrative news writing, exactly the kind of content 
needed for embedding-based bias measurement. Result count of 1.3M+ articles 
in one regional Newsstream confirms substantial volume.

**Implications for corpus map:**
- 1985–present content is available through NJIT — this addresses the modern gap
- Hispanic Newsstream covers the Spanish-language press concern flagged in the 
  proposal (TX, CA, FL, NM)
- However: the standard ProQuest web interface allows reading/saving individual 
  articles only — NOT bulk extraction. Saving articles as PDFs to build a corpus 
  would violate NJIT's license terms and is not viable
- For computational use, need TDM Studio (ProQuest's hosted Jupyter environment) 
  or a negotiated bulk-export agreement

### TDM Studio trial requested

**Action:** Submitted TDM Studio trial request through NJIT ProQuest access.

**Framing used:**
- Use: Compute word embeddings and gender bias scores (WEAT, relative norm 
  distance) from full-text U.S. newspaper articles. Only derived statistical 
  outputs (embeddings, bias scores) will be exported; no article text.
- Topic: Measuring state-level gender bias in U.S. public discourse, 
  1900–present, using computational text analysis.

**Affiliation:** NJIT alumna (continued library access).

**Status:** Pending response. Expected 2–5 business days.

**Important behavioral note:** While the trial is pending, no bulk-extraction 
activity from the alumni-access ProQuest account. ProQuest detects systematic 
downloading and reviews account behavior — keeping activity clean improves 
trial approval odds.

### Updated corpus map

| Period | Source | Status |
|---|---|---|
| 1900–1963 | Chronicling America | ✓ Free, accessible |
| 1964–1984 | ProQuest Historical Newspapers | ✗ Not visible in NJIT's 7 databases — need to check with librarian |
| 1985–2014 | NJIT U.S. Newsstream (via TDM Studio) | ⚠️ Content confirmed; computational access pending TDM trial |
| 2015–present | GDELT BigQuery (set up 2026-05-15) | ✓ URL/metadata access ready; article text fetching is separate step |

### Outstanding questions

1. **TDM Studio trial outcome** — wait for ProQuest/NJIT response (2–5 days)
2. **ProQuest Historical Newspapers availability at NJIT** — need to email 
   reference librarian to confirm whether NJIT has this (covers 1964–1984)


### Process note for future sessions

Today included a redundant Common Crawl exploration that could have been avoided 
by checking the existing project state (specifically the GDELT BigQuery setup 
done 2026-05-15). For future corpus-related decisions, the first move should 
be reviewing what's already in place before adding new sources.

### Congressional Record — end-to-end demo working

**Path that works:** GovInfo API at the granule level, specifically:
- `/packages/{packageId}/granules` to list speeches in a day
- `/packages/{packageId}/granules/{granuleId}/summary` for speaker metadata
- The `txtLink` from the granule summary for the speech text

**Path that doesn't work (verified):**
- GovInfo bulk data at /bulkdata/CREC/ — returns "content not found" (CREC 
  not in the bulk data offerings)
- `/published/{date}/{date}` API endpoint with collection filter — returns 0
- `/collections/CREC/{start}/{end}` API endpoint — returns 0

**Demo executed:**
- Pulled package CREC-2024-03-12 (one day of House proceedings, 197 granules)
- Filtered to a substantive speech granule (CREC-2024-03-12-pt1-PgH1097-4)
- Confirmed metadata: speaker = Vasquez (D-NM, House), BioGuide V000136
- Confirmed full speech text retrievable via txtLink

**Implications for project:**
- State-year mapping for political speech is essentially solved at the API 
  level — no inference required, GovInfo returns the state attribute directly
- Daily Edition (CREC) covers 1995–present cleanly
- Bound Edition (CRECB, 1873–1994) is PDF-based; Democracy-Lab parser handles 
  it with caveats — would need separate effort
- For convergent validation against newspaper bias scores, 1995+ data is 
  more than enough

**Demo files saved at:** 
`code/congressional_record_scraper/cr_minimal_demo.ipynb`

**Next steps when CR work resumes:**
- Build a loop over all session days in a target year
- For each granule with members≥1, pull text + speaker state
- Bucket by state-year
- Train embeddings per state-year cell (validation corpus)
- Compute bias scores
- Compare with newspaper-derived bias scores (convergent validity test)

**Note on demo approach:** The demo bypassed the cloned Democracy-Lab 
parser and called the GovInfo API directly. This worked for the simple 
case (granule with members metadata in API summary) but doesn't handle 
multi-speaker sections, procedural granules, or pre-1994 PDF content. 
Democracy-Lab parser remains the right tool for production-scale CR 
corpus building. The cloned repo stays in `code/congressional_record_scraper/uscongress-data/` 
for when production work begins.

## 2026-06-04 — Security cleanup, Git housekeeping, ready to begin extraction

### What changed today

- Migrated GovInfo API key out of notebooks into `.env` file at project root
- Updated `cr_test.ipynb` and `cr_minimal_demo.ipynb` to load `API_KEY` via `python-dotenv`
- Regenerated GovInfo API key (previous key exposed earlier in session)
- Cleared output cells in notebooks to avoid leaking key in stored output
- Added `.env`, `secrets.json`, `venv/`, `uscongress-data/`, and data folders to `.gitignore`
- Committed and pushed demo notebooks to GitHub (`gender_bias_in_usa` branch)

### Status of corpus sources (as discussed with Gineete)

| Source | Status |
|---|---|
| GSS | Downloaded; processing pending |
| Newsstream | NJIT access confirmed; awaiting TDM Studio trial response |
| TDM Studio | Trial requested, no response yet |
| Congressional Record | API path verified; full January 2024 extraction starting now |
| GDELT BigQuery | Access set up; extraction starting next |
| Chronicling America | Source verified accessible; extraction starting after GDELT |
| Reddit (PullPush) | Path verified; greenlit by Gineete; multi-week extraction to start in background |
| Twitter | No free realistic path identified — recommended skip; awaiting Gineete confirmation |
| ProQuest Historical Newspapers (1964–1984) | NJIT availability not yet confirmed; librarian inquiry not sent |

### Deadline / commitment

Gineete asked for an early demo by Friday EOD US time (so by Saturday morning IST). Plan:
- **Wed/Thu**: Extract small slices from Chronicling America, GDELT, Congressional Record; kick off Reddit in background; process GSS
- **Fri**: Build dashboard/notebook combining what's extracted so far, with bias scores on the small slice — focus on showing pipeline working end-to-end

### Outstanding decisions

- Whether to use uscongress-data parser (cloned but not in Git) or hand-rolled API code for production CR extraction
- Whether to send the librarian inquiry about ProQuest Historical Newspapers
- Whether to use full historical Reddit (multi-week processing) or PRAW forward-only for the demo

### Congressional Record — January 2024 extraction complete
- 547 single-speaker speeches extracted (filtered from 1,528 floor granules)
- 51 unique states + DC represented
- 397,726 total words, range 346–242,825 chars per speech
- Distribution heavy in big states (NY=112, CA=45), thin in small states (MS/NH/DE/ME=1)
- Methodology note: small-state cells will need time aggregation for stable embeddings

## 2026-06-05 — GDELT article text fetch completed

**Source:** GDELT 2.0 Global Knowledge Graph via BigQuery (project: bias-project-gdelt)
**Target period:** January 2024
**Sample:** 1,530 URLs (30 per state × 51 states)

**Fetch results:**
- Successful (real text): ~690 articles
- Fetch failed (403/timeout/block): 828
- Paywall stubs: 1
- No text extracted: 0
- Total runtime: 127.5 minutes

**Success rate:** ~45% — lower than the 60-80% projected range
**Usable coverage:** ~13 articles per state on average

**Output files:**
- `corpus/gdelt/2024-01/gdelt_articles_with_text.csv` — articles with text
- `corpus/gdelt/2024-01/fetch_errors.log` — failed URL log

**Key finding:** Failure pattern is consistent with domain-level bot blocking —
failures increased steadily from 40% in early batches to 54% overall. Zero
paywall stubs suggests hard blocks (403/timeout) rather than soft paywalls.
This confirms the GDELT URL-fetch engineering risk documented in the earlier
session. 690 articles is sufficient for a demo but insufficient for a
production-grade state-year corpus. Mitigation options: user-agent rotation,
residential proxies, or supplementing with a source that provides full text
directly (Congressional Record, Chronicling America, Reddit).

**Status:** Complete for January 2024 demo slice. Full-scale extraction
deferred pending evaluation of fetch success rate improvement strategies.

## 2026-06-05 — Chronicling America extraction completed

**Source:** Library of Congress Chronicling America via loc.gov API
**Target period:** 1920, 1921, 1922
**States:** OH, WY, CA, TX, IL, MS, MT, OR, NY (9 states)
**Cap:** 50 pages per state-year cell

**Results:**
- Total pages fetched: 1,350
- No text extracted: 163 (12% — normal for OCR pages)
- All 27 cells (9 states × 3 years) fully populated at 50 pages each

**Output files:**
- `corpus/chronicling_america/1920-1922/articles.csv` — page-level OCR text
- `corpus/chronicling_america/1920-1922/errors.log` — pages with no text

**Key technical notes:**
- Legacy chroniclingamerica.loc.gov API is dead (403 Cloudflare block)
- New loc.gov API used with `dl=page` filter for page-level results
- OCR text is returned directly in the `description` field of API response
  — no separate OCR fetch needed
- Multi-word state names require spaces not hyphens (e.g. 'new york' not
  'new-york') — confirmed via debug testing
- Date filter works correctly with `start_date`/`end_date` parameters

**Status:** Complete for 1920–1922 demo slice. Full 50-state extraction
and extension to full 1900–1963 range deferred until after Friday demo.

---

## 2026-06-05 — Reddit/PullPush extraction completed

**Source:** PullPush API (https://api.pullpush.io) — community successor to Pushshift
**Target period:** January 2020
**States:** All 50 states (state subreddits)
**Cap:** 200 posts + 200 comments per state

**Results:**
- Total posts: 4,423
- Total comments: 4,563
- Total items: 8,986
- Average per state: ~180 items
- All 50 states covered with usable data

**Output files:**
- `corpus/reddit/2020-01/posts.csv` — submissions with title + selftext
- `corpus/reddit/2020-01/comments.csv` — comments with body text
- `corpus/reddit/2020-01/errors.log` — fetch errors

**Key technical notes:**
- PullPush API requires no API key, no authentication
- Submissions are mostly link posts (title-only text); selftext thin
- Comments provide the bulk of usable text (~80-95% non-deleted per state
  confirmed in verification testing across 9 states)
- Small states (WY, VT, ND) have lower volume but still returned usable data
- Deleted/removed content filtered out during extraction
- Rate limit: 1.5s delay between requests, no throttling encountered

**Status:** Complete for January 2020 demo slice. Full historical extraction
(2011–present, all 50 states) deferred — estimated 3–6 weeks background
processing time. Reddit greenlit by Gineete as a corpus source.

---

## 2026-06-05 — GSS validation data processed

**Source:** GSS Data Explorer (gssdataexplorer.norc.org)
**File:** `validation_data/gss/gss_gender_attitudes.xlsx`
**Variables:** FEFAM, FEPRES, FEWORK, FECHLD, FEHELP, FEPOL, FEHIRE,
               YEAR, REGION_7222, REG16_7222 (+ demographics)
**Rows:** 75,699 respondents, 1972–2024

**Processing steps:**
- Replaced GSS missing value codes (-100, -99, -98, -97, -96, -90, -89, -70)
  with NaN
- Filtered out region code -70 (not applicable)
- Computed region-year means for all 7 attitude variables
- Added region labels (9-category REGION_7222)
- Computed composite gender attitude score (mean across available variables)
- Dropped region-year cells with no valid responses

**Results:**
- Valid attitude responses: 47,516 out of 75,699 (63%)
- Clean region-year panel: 261 cells (9 regions × years 1972–2022)
- National trend: composite score rises from ~1.3 (1972) to ~2.5 (2021)
  indicating progressive shift toward less traditional gender attitudes
- Variable coverage: fepol 93%, fefam/fechld 79%, fepres 66%, fework 59%,
  fehire 45%, fehelp 38%

**Output files:**
- `validation_data/gss/processed/gss_region_year_clean.csv` — main panel
- `validation_data/gss/processed/gss_region_year_means.csv` — raw means
- `validation_data/gss/processed/gss_national_trend.csv` — national averages

**Status:** Complete. Ready for validation once bias scores are computed.

## 2026-06-07 — Embedding pipelines completed (all three methodologies)

### Word2Vec + WEAT6
- Trained per-state Word2Vec models on combined corpus (CR + CA + GDELT + Reddit)
- min_count=1 to maximize WEAT word coverage
- **States scored: 28 out of 50**
- **Gap states (22):** AL, AZ, CO, DE, FL, ID, KS, MO, MT, NH, NJ, NM, OK, PA, RI, SD, TN, UT, VT, WA, WI, WV
- Gap reason: WEAT word list terms absent from small per-state corpus
- Gap documented in `outputs/embeddings/word2vec/weat6_gap_documentation.json`
- Score range: -0.057 to +0.050 (mixed directions)
- Output: `outputs/embeddings/word2vec/weat6_scores_word2vec.csv`

### GloVe + WEAT6 (corpus-weighted pretrained GloVe)
- Used pretrained GloVe 6B 100d vectors (downloaded to `models/glove/`, excluded from Git)
- Corpus-weighted approach: pretrained vectors weighted by state-level word frequencies
- Mittens fine-tuning abandoned — prohibitive runtime (50+ minutes for partial run)
- Corpus-weighted GloVe is the practical alternative at demo corpus scale
- **All 50 states scored**
- Global GloVe baseline: 0.2165 (male→career)
- Score range: 0.09 to 0.26 (all male→career)
- Output: `outputs/embeddings/glove/weat6_scores_glove.csv`

### BERT + SEAT
- Used pretrained bert-base-uncased (HuggingFace, ~440MB, cached locally)
- SEAT approach: contextual embeddings from real corpus sentences per state
- Template: sentences containing each WEAT word sampled from state corpus (5 per word)
- **All 50 states scored**
- Global BERT baseline: 0.0063 (male→career)
- Score range: -0.009 to +0.039 (44 male→career, 6 female→career)
- Output: `outputs/embeddings/bert/seat_scores_bert.csv`

**Key technical notes:**
- GloVe 6B 100d file (331MB) excluded from Git via .gitignore — download from Stanford NLP
- git filter-branch used twice to remove GloVe file from commit history
- All BERT processing on CPU — no GPU available; runtime ~20 minutes for 50 states
- Word2Vec gap states will be resolved with full-scale extraction (more text per state)

## 2026-06-18 — Era-name coverage check (Word2Vec corpus)

**Question:** Do the era-specific SSA name lists actually appear in the demo
corpus often enough to matter for scoring?

**Method:** Counted era-name presence and frequency over the same tokenized
(state, period) cells Word2Vec scored on (gensim simple_preprocess), via Cell 11
of `word2vec_weat.ipynb`. Periods mapped: hist_1920s→historical_1920s,
modern_2020/modern_2024→modern_2024.
**Output:** `outputs/validation/era_name_coverage.csv`

**Results (mean per 10k tokens):**
| period       | male hits/10k | female hits/10k | male cov% | female cov% |
|--------------|---------------|-----------------|-----------|-------------|
| hist_1920s   | 29.86         | 6.44            | 37.2      | 12.2        |
| modern_2020  | 4.20          | 2.03            |  7.5      |  2.7        |
| modern_2024  | 16.25         | 3.70            | 36.9      | 14.6        |

- 158 of 222 (state, period, sex) groups have >=1 era name present.
- All zero-coverage cells are modern_2020 (Reddit) — conversational text is not
  name-dense.

**Findings (not bugs):**
- Coverage is real, NOT near-zero (unlike Caliskan name lists). Names DO appear.
- Male coverage ~4-5x female across all periods. News/Congressional text names
  more men; female mentions spread across a longer tail outside the top-20 list.
  Consistent with the documented male-name temporal-stability effect.
- Reddit (modern_2020) too sparse for stable name-based WEAT scoring.

**Deliverable status (Gineete Section 7.2):** Built and coverage-validated.
Usable as a SUPPLEMENTARY signal in name-dense corpora (news, Congressional
Record). Female side and social-media (Reddit) coverage require full-scale
extraction before name-based scoring is stable.


## 2026-06-18 — Period-split re-scoring (GloVe + BERT) + composite z-scores

### All four methods now period-split & aligned
Discovered GloVe and BERT saved CSVs still used the deprecated mixed_demo
single-cell-per-state design. Re-ran both period-split; Word2Vec and RoBERTa
were already correct. All four now use Garg pronoun pairs, Career-Family
(WEAT6/SEAT), (state, period) cells, sign convention positive = male->career.

| Method   | File                          | Score column        | Cells |
|----------|-------------------------------|---------------------|-------|
| Word2Vec | weat6_scores_word2vec_v2.csv  | weat6_pairs_d       | 38    |
| GloVe    | weat6_scores_glove_v2.csv     | weat6_d             | 81    |
| BERT     | seat_scores_bert_v2.csv       | seat_career_family  | 108   |
| RoBERTa  | seat_scores_roberta.csv       | seat_career_family  | 108   |

- BERT re-run also switched [CLS] -> mean-pooling, so BERT vs RoBERTa 2x2 is
  now unconfounded (both mean-pooled, same targets, 108 cells each).
- GloVe per-period means (all positive): hist_1920s 0.78, modern_2020 0.52,
  modern_2024 0.83. BERT: 7/2, 31/19, 37/12 male->career by period.

### Composite z-scores — DONE
- code/embeddings/composite_scores.ipynb -> outputs/composite/composite_scores.csv
- Each method z-scored within itself (mean 0, sd 1) to remove scale differences
  (GloVe raw mean +0.71 vs RoBERTa +0.001 — z-scoring equalizes contribution).
- Composite = mean of available method z-scores; require >=2 methods; n_methods
  recorded per cell. Coverage: 108 cells (38 with 4 methods, 43 with 3, 27 with 2).
- Period means (relative, within-dataset): hist_1920s -0.195, modern_2020 -0.120,
  modern_2024 +0.217.
- Caveat: composite_z is a RELATIVE ranking across cells, not absolute bias level.
  Pipeline deliverable — construction correct, but weak inter-method correlation
  at demo scale means substantive values not yet interpretable. Ready for full-scale.

### Era-name coverage check — DONE (earlier today)
- outputs/validation/era_name_coverage.csv. Names present but male-skewed (~4-5x
  female); Reddit sparse. Supplementary at demo scale; full extraction for the rest.

### Pending
- Permutation-test p-values (next)
- Inter-method correlation matrix (quantify the "weak" claim)
- Duncan Dissimilarity Index — IPUMS extract scope sent to Gineete, awaiting reply


## 2026-06-18 — Period-split re-scoring (GloVe + BERT) + composite z-scores

### All four methods now period-split & aligned
Found that the saved GloVe and BERT CSVs still used the deprecated mixed_demo
design (one cell per state, all periods merged). Re-ran both period-split.
Word2Vec and RoBERTa were already correct. All four now use Garg pronoun pairs,
Career-Family (WEAT6 / SEAT), (state, period) cells, sign convention
positive = male->career.

| Method   | File                          | Score column        | Cells |
|----------|-------------------------------|---------------------|-------|
| Word2Vec | weat6_scores_word2vec_v2.csv  | weat6_pairs_d       | 38    |
| GloVe    | weat6_scores_glove_v2.csv     | weat6_d             | 81    |
| BERT     | seat_scores_bert_v2.csv       | seat_career_family  | 108   |
| RoBERTa  | seat_scores_roberta.csv       | seat_career_family  | 108   |

- BERT re-run also switched [CLS] -> mean-pooling, so the BERT vs RoBERTa 2x2 is
  now unconfounded (both mean-pooled, same targets, 108 cells each).
- GloVe per-period means (all positive): hist_1920s 0.78, modern_2020 0.52,
  modern_2024 0.83.
- BERT by period (male->career / female->career): hist_1920s 7/2,
  modern_2020 31/19, modern_2024 37/12.

### Composite z-scores — DONE
- code/analysis/composite_scores.ipynb -> outputs/composite/composite_scores.csv
- Each method z-scored within itself (mean 0, sd 1) before combining, to remove
  scale differences (raw means: GloVe +0.71, Word2Vec +0.004, BERT +0.007,
  RoBERTa +0.001 — z-scoring equalizes their contribution).
- Composite = mean of available method z-scores per cell; require >=2 methods;
  n_methods recorded per cell.
- Coverage: 108 cells, all with >=2 methods (38 with all 4, 43 with 3, 27 with 2).
- Period means (relative, within-dataset): hist_1920s -0.195,
  modern_2020 -0.120, modern_2024 +0.217.
- CAVEAT: composite_z is a RELATIVE ranking across cells, not an absolute bias
  level. Pipeline deliverable — construction is correct, but weak inter-method
  correlation at demo scale means substantive values are not yet interpretable.
  Ready for full-scale corpus.

### Era-name coverage check — DONE
- code/embeddings/word2vec_weat.ipynb (Cell 11) ->
  outputs/validation/era_name_coverage.csv
- Era names present in corpus but male-skewed (~4-5x female across periods);
  Reddit (modern_2020) sparse, all zero-coverage cells are Reddit.
- Conclusion: supplementary signal in name-dense corpora (news, Congressional);
  female side + social media need full-scale extraction. Satisfies Section 7.2.

### Era-specific SSA name lists — DONE (earlier)
- Built from SSA national data via GitHub mirror hackerb9/ssa-baby-names
  (SSA server hard-blocks programmatic access). Birth-cohort windows:
  historical_1920s = 1880-1900, modern_2024 = 1950-2005. Top-20 male/female
  per era, single-sex purity >=0.95. Output: word_lists/era_names/

### Pending
- Permutation-test p-values: code/embeddings/permutation_tests.ipynb exists from
  an earlier session — needs review + repoint to the _v2 score files (next task).
- Inter-method correlation matrix: code/validation/cross_model_consistency.ipynb
  exists — check whether it already covers this before adding anything.
- Duncan Dissimilarity Index — IPUMS account created; extract scope (1920 census +
  recent ACS, OCC1950 harmonized, demo-scope) sent to Gineete, awaiting reply.
  Data will land in validation_data/census_acs/.

  ### Permutation-test p-values (Word2Vec) — DONE
- code/embeddings/permutation_tests.ipynb ->
  outputs/embeddings/word2vec/permutation_tests_word2vec.csv
- Method: Caliskan (2017) WEAT permutation test. Pool gender target words
  (male_pairs + female_pairs), repartition randomly, recompute statistic;
  one-sided p = (count >= observed + 1)/(n_perm + 1). 1000 permutations/cell,
  single seed=42 model. Attribute sets (career/family) held fixed.
- Tested 40 of 111 cells (others dropped by <50-sentence / coverage filters).
- Significant: 4 at p<0.01, 6 at p<0.05 (15%), 7 at p<0.10.
- Finding: only ONE substantive significant cell (CA modern_2024, stat +0.2477,
  p=0.003 — most name/career-dense cell). Remaining "significant" cells have
  near-zero statistics with low p = tight-null artifact of small-corpus
  instability (e.g. OK stat -0.0017, p=0.006). 5 of 7 sub-0.10 cells are Reddit
  (sparsest corpus). 15% vs 5% chance floor = modest signal, not robust.
- Consistent with the corpus-size story. Test is correct; data is thin.
  Word2Vec only — GloVe/BERT/RoBERTa permutation deferred.

### Cross-model consistency (inter-method correlation) — DONE
- code/validation/cross_model_consistency.ipynb ->
  outputs/validation/cross_model_merged_scores.csv + cross_model_consistency.json
- Spearman rho on 38 cells with all 4 methods present (period-split _v2 scores),
  framed per Gineete Sec 4.2 thresholds.
- BERT-RoBERTa (contextual): rho = 0.917, p<0.001 — STRONG agreement, clears
  >0.6 bar. Validates the SEAT pipeline; confirms the BERT mean-pooling re-run
  gave a clean, unconfounded 2x2.
- Word2Vec-GloVe (static): rho = 0.150 — diverge (<0.4). Driven by train-from-
  scratch (W2V, ~3k words/cell, noisy) vs pretrained-restricted (GloVe, stable
  external associations), not a true bias disagreement.
- Cross-family pairs (static vs contextual): rho ~ 0 (-0.01 to -0.10), all n.s.
- Takeaway: contextual pipeline internally validated; static side corpus-size-
  limited; cross-family comparison needs full-scale data. Framework is
  operational and discriminating as designed.

### Demo analysis suite status
- Composite z-scores: DONE (code/analysis/composite_scores.ipynb)
- Permutation p-values (Word2Vec): DONE
- Cross-model consistency: DONE
- Era-specific name lists + coverage check: DONE
- Duncan Dissimilarity Index: BLOCKED — IPUMS extract scope (1920 census +
  recent ACS, OCC1950, demo-scope) sent to Gineete, awaiting reply.
  Data will land in validation_data/census_acs/.

### Overarching demo narrative (consistent across all analyses)
Methods are implemented correctly and the pipeline runs end to end. At demo
corpus scale (~100x smaller than Garg): contextual models agree strongly,
static side is unstable, inter-method and GSS correlations are weak, permutation
significance is sparse/artifactual, era-name coverage is thin. This is a
documented corpus-size finding and the evidence base for full-scale extraction,
not a methodology failure.

### GSS validation re-run (period-split, modern-only) — DONE
- code/validation/validation.ipynb -> outputs/validation/gss_validation_by_period.csv
- Fixed prior flaw: old run merged mixed-period scores vs 2010-2022 GSS. Now uses
  period-split _v2 scores, modern cells only (GSS starts 1972, can't validate 1920),
  reported separately for modern_2020 and modern_2024, all 4 methods.
- Result: no significant correlation (all p>0.39). Most coefficients lean weakly
  NEGATIVE = expected direction (more bias <-> more traditional). Best: w2v
  modern_2020 r=-0.148. w2v modern_2024 skipped (only 3 states).
- Caveats unchanged: region-level GSS (9 values / 50 states) limits power; demo
  corpus ~100x below published scale. Framework built, ready to rerun at full scale.
- Dropped redundant inter-method cell (now in cross_model_consistency.ipynb).