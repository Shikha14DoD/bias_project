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