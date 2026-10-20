# GSS Validation Data Processing

## Purpose

Processes General Social Survey gender attitude data into region-year
aggregates for validating the gender bias state-year panel scores.

## Source

- **GSS Data Explorer** (gssdataexplorer.norc.org)
- Variables: FEFAM, FEPRES, FEWORK, FECHLD, FEHELP, FEPOL, FEHIRE
- Coverage: 1972–2024
- Respondents: 75,699

## Key variables

| Variable | Question summary |
|---|---|
| FEFAM | Women should take care of home, not country |
| FEPRES | Would vote for female president |
| FEWORK | Approve of married woman working |
| FECHLD | Working mother relationship with children |
| FEHELP | Women help themselves, not special favours |
| FEPOL | Women not suited for politics |
| FEHIRE | Men hired over women in scarce jobs |

## Missing value codes

GSS uses negative codes for missing data — must be replaced with NaN
before analysis: -100, -99, -98, -97, -96, -90, -89, -70

## Output files

| File | Description |
|---|---|
| `gss_region_year_clean.csv` | 261 region-year cells, cleaned, with composite score |
| `gss_region_year_means.csv` | Raw region-year means before cleaning |
| `gss_national_trend.csv` | National yearly averages 1972–2022 |

## Key finding

Composite gender attitude score rises from ~1.3 (1972) to ~2.5 (2021),
confirming a 50-year national shift toward less traditional gender attitudes.
This trend should correlate with declining bias scores from the embedding
pipeline — providing the primary external validation for the project.

## Key files

| File | Description |
|---|---|
| `code/gss/gss_processing.ipynb` | Processing notebook |
| `validation_data/gss/gss_gender_attitudes.xlsx` | Raw GSS download |
| `validation_data/gss/processed/` | All processed outputs |