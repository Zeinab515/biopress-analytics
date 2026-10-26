# Data Audit — hand_hygiene_data_labeled.csv

Source: Kolola & Gezahegn (2017), Debre Berhan referral hospital, Ethiopia. Raw file kept unmodified in `data/raw/` (read-only).

## Shape and quality
- 917 rows x 8 columns; 0 exact duplicate rows.
- Complied = Yes: 202; No: 715. Compliance = 22.03% (matches the published 22.0%).
- `Opp` runs 1..917 in file order, but id **788 appears twice** and id **787 is absent** (probable typo). Treated as an observation sequence only.
- Missing values: HHaction 715, Missedbutglove 202 (structural, see below). All other columns complete.

## Target leakage (confirmed)
| Column | Finding | Decision |
|---|---|---|
| HHaction | Empty in all 715 `No` rows; filled in all 202 `Yes` rows | **Exclude** from models |
| Missedbutglove | Empty in all 202 `Yes` rows; filled in all 715 `No` rows (Yes 307 / No 408) | **Exclude**; descriptive use among non-compliant only |
| Opp | Sequential observation id | **Exclude**; not a feature |

## Allowed model features
`Ward`, `Profcat`, `Shift`, `Indication`.

## Compliance by group (n, rate, Wilson 95% CI)
| Dimension | Group | n | Rate |
|---|---|---|---|
| Indication | After body fluid exposure | 149 | 75.8% (68.4–82.0) |
| | After patient contact | 166 | 42.8% (35.5–50.4) |
| | After contact with patient surroundings | 152 | 3.3% (1.4–7.5) |
| | Before an aseptic procedure | 195 | 3.6% (1.7–7.2) |
| | Before patient contact | 255 | 2.4% (1.1–5.0) |
| Ward | NICU 27.3%, Paediatric 26.5%, Medical 21.3%, Ob/Gyn 19.6%, Surgical 18.7% | 77–219 | CIs overlap |
| Shift | Morning 23.3%, Night 22.6%, After noon 20.1% | 230–369 | CIs overlap |
| Profcat | Other 23.2%, Nurse 22.9%, Midwife 21.2%, Medical doctor 20.6% | 56–476 | CIs overlap |

Chi-square tests of independence with Complied: Indication p < 0.001; Ward p = 0.21; Shift p = 0.59; Profcat p = 0.89.
Only Indication shows a detectable association.

## Structural notes
- Midwife appears only in Ob/Gyn, so Ward and Profcat are confounded.
- No worker id, session id or date: observations may be clustered (same observer/worker), so CV estimates may be optimistic.
- Single hospital, ~one week of observation; Hawthorne effect likely inflates observed compliance.

## Baseline model check (5-fold stratified CV, seed 0)
| Features | LogReg ROC-AUC | RF ROC-AUC |
|---|---|---|
| Indication only | 0.886 | 0.886 |
| Ward+Profcat+Shift+Indication | 0.907 | 0.923 |
| Ward+Profcat+Shift (no Indication) | 0.50 | 0.53 |
| DummyClassifier | 0.50 | |

Interpretation: signal comes almost entirely from Indication. Prefer Logistic Regression.

## Decision
Data approved for Phase 1 with the feature list above. Re-run the audit if the file changes.
