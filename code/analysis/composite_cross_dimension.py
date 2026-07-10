"""
Cross-DIMENSION composite per methodology doc Section 2.4.

Averages the four BIAS DIMENSIONS (not the four embedding models):
  1. Career-Family   2. Competence-Warmth   3. Leadership-Subordination   4. Occupation

*** SIGN ALIGNMENT (per Ginette's 2.4 comment) ***
All four dimensions MUST point the same way ("positive = male-advantaged /
more traditional bias") before z-scoring, or they partially cancel.

Audited sign of each dimension:
  - Career-Family  (WEAT): weat_effect_size(male, female, career, family)
       -> positive = male->career               ALIGNED (no flip)
  - Competence-Warmth (WEAT): weat_effect_size(male, female, competence, warmth)
       -> positive = male->competence            ALIGNED (no flip)
  - Leadership-Subordination (WEAT): weat_effect_size(male, female, leadership, subordination)
       -> positive = male->leadership            ALIGNED (no flip)
  - Occupation (Garg RND): ||occ - v_male|| - ||occ - v_female||
       -> positive = occupation closer to FEMALE  *** OPPOSITE -> FLIP SIGN ***

So the three WEAT dimensions pass through unchanged; Occupation is NEGATED to
align to the canonical "positive = male-advantaged" direction.
(The global canonical direction is Ginette's pending sign-convention decision;
whichever she picks is one final global negation on top -- it does not change
this internal alignment.)

DEMO-SCALE CAVEAT: yields only ~3 cells with >=3 dimensions, because Measures 2/3
are sparse and Occupation is currently PERIOD-level (states pooled) so it cannot
join on (state, period). Occupation join below is written but will only populate
once occupation is scored per (state, period) at full scale.
"""
import pandas as pd
import numpy as np
from pathlib import Path

BASE = Path(r"D:\Shikha\bias_project")
OUT  = BASE / "outputs" / "composite" / "composite_cross_dimension.csv"

# --- Dimension 1: Career-Family (per-cell; already mean of 4 model z-scores) ---
cf = pd.read_csv(BASE / "outputs" / "composite" / "composite_scores.csv")
cf = cf[["state", "period", "composite_z"]].rename(columns={"composite_z": "dim_career_family"})

# --- Dimensions 2 & 3: Competence-Warmth, Leadership-Subordination (Word2Vec) ---
m23 = pd.read_csv(BASE / "outputs" / "embeddings" / "word2vec" / "measures23_scores_word2vec.csv")
cw = (m23[m23["compwarm_reliable"] == True][["state", "period", "compwarm_d"]]
      .rename(columns={"compwarm_d": "dim_competence_warmth"}))
ls = (m23[m23["leadsub_reliable"] == True][["state", "period", "leadsub_d"]]
      .rename(columns={"leadsub_d": "dim_leadership_subordination"}))

comp = (cf.merge(cw, on=["state", "period"], how="outer")
          .merge(ls, on=["state", "period"], how="outer"))

# --- Dimension 4: Occupation — SIGN-FLIPPED to align (positive = male-advantaged) ---
# Occupation is currently period-level (states pooled). This join is written for
# full scale, where occupation is scored per (state, period). At demo scale it
# adds no cells (no state key to join on) but documents the required flip.
try:
    occ = pd.read_csv(BASE / "outputs" / "embeddings" / "occupation" / "occupation_rnd_scores.csv")
    if "state" in occ.columns and "period" in occ.columns:
        # pick the RND score column (adjust name if your file differs)
        score_col = next((c for c in occ.columns if "rnd" in c.lower() or "score" in c.lower()), None)
        if score_col:
            occ = occ[["state", "period", score_col]].copy()
            occ["dim_occupation"] = -occ[score_col]   # <-- SIGN FLIP: female-assoc(+) -> male-advantaged(+)
            occ = occ[["state", "period", "dim_occupation"]]
            comp = comp.merge(occ, on=["state", "period"], how="outer")
        else:
            print("Occupation: no RND score column found; skipping (period-level at demo scale).")
    else:
        print("Occupation: period-level (no state key) — cannot join per-cell at demo scale. "
              "Sign-flip is baked in for full scale.")
except FileNotFoundError:
    print("Occupation file not found; skipping.")

# Which dimension columns are present
dims = [c for c in ["dim_career_family", "dim_competence_warmth",
                    "dim_leadership_subordination", "dim_occupation"] if c in comp.columns]

# z-score each dimension across its available cells (Section 2.4), then average
for d in dims:
    comp[d + "_z"] = (comp[d] - comp[d].mean()) / comp[d].std(ddof=1)

zcols = [d + "_z" for d in dims]
comp["n_dimensions"]          = comp[zcols].notna().sum(axis=1)
comp["composite_dimension_z"] = comp[zcols].mean(axis=1, skipna=True)
comp["flag_underpowered"]     = comp["n_dimensions"] < 3   # doc 2.4 rule

comp = comp.sort_values(["period", "state"])
OUT.parent.mkdir(parents=True, exist_ok=True)
comp.to_csv(OUT, index=False)

print(f"Saved {OUT}")
print(f"Dimensions included: {dims}")
print(f"Total cells: {len(comp)}")
print(comp["n_dimensions"].value_counts().sort_index().to_string())
print(f"Cells meeting doc >=3-dimension bar: {(comp['n_dimensions'] >= 3).sum()}")