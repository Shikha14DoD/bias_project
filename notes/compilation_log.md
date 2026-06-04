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
