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