# Embedding Pipelines — Gender Bias Scoring

## Purpose

Trains word/sentence embeddings on state-level corpus text and computes
WEAT/SEAT gender bias scores for each state. Three methodologies are
implemented for robustness and cross-validation.

## Methodologies

### 1. Word2Vec + WEAT6 (`word2vec_weat.ipynb`)
- Trains a separate Word2Vec model per state corpus
- Computes WEAT 6 (Career–Family bias) using Caliskan (2017) word lists
- Static embeddings trained from scratch on project corpus
- **Limitation:** requires sufficient per-state vocabulary — 22 gap states
  at demo scale due to small corpus size

### 2. GloVe + WEAT6 (`glove_weat.ipynb`)
- Uses pretrained GloVe 6B 100d vectors (Stanford NLP)
- Corpus-weighted scoring: pretrained vectors weighted by state word frequencies
- All 50 states scored — no vocabulary gap problem
- **Note:** Mittens fine-tuning was tested but abandoned (prohibitive runtime
  at demo corpus scale; revisit after full-scale extraction)

### 3. BERT + SEAT (`bert_seat.ipynb`)
- Uses pretrained bert-base-uncased (HuggingFace)
- SEAT (Sentence Encoder Association Test) — contextual embeddings
- Real corpus sentences used per state for contextual scoring
- All 50 states scored; more nuanced than static methods

## Word Lists

All word lists from `word_lists/caliskan_2017/`:

| File | Contents |
|---|---|
| `career_terms_weat6.txt` | executive, management, salary, ... |
| `family_terms_weat6.txt` | home, parents, children, ... |
| `male_names_weat6.txt` | john, paul, mike, ... |
| `female_names_weat6.txt` | amy, joan, lisa, ... |

## Output Files

| File | Method | States | Notes |
|---|---|---|---|
| `outputs/embeddings/word2vec/weat6_scores_word2vec.csv` | Word2Vec | 28 | 22 gap states |
| `outputs/embeddings/word2vec/weat6_gap_documentation.json` | Word2Vec | — | Gap documentation |
| `outputs/embeddings/glove/weat6_scores_glove.csv` | GloVe | 50 | All states |
| `outputs/embeddings/bert/seat_scores_bert.csv` | BERT | 50 | All states |

## Score Interpretation

**WEAT6 / SEAT score > 0** → male names more associated with career terms (male→career bias)
**WEAT6 / SEAT score < 0** → female names more associated with career terms (female→career bias)

| Method | Global Baseline | State Range |
|---|---|---|
| Word2Vec | — | -0.057 to +0.050 |
| GloVe | +0.2165 | +0.09 to +0.26 |
| BERT | +0.0063 | -0.009 to +0.039 |

## External Model Files

- **GloVe:** Download `glove.6B.zip` from https://nlp.stanford.edu/data/glove.6B.zip
  — extract `glove.6B.100d.txt` to `models/glove/` (excluded from Git, 331MB)
- **BERT:** Downloaded automatically via HuggingFace on first run (~440MB, cached)

## Key References

- Caliskan et al. (2017) — WEAT methodology and word lists
- Garg et al. (2018) — historical bias measurement framework
- May et al. (2019) — SEAT methodology for contextual models