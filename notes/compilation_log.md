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