# Data Dictionary

| Column | Type | Values | Meaning (as understood) | Model use |
|---|---|---|---|---|
| Ward | category | Ob/Gyn, Paediatric, Medical, Surgical, NICU | Ward of observation | Allowed |
| Profcat | category | Nurse, Medical doctor, Midwife, Other | Professional category | Allowed |
| Shift | category | Morning, After noon, Night | Shift of observation | Allowed |
| Opp | int | 1..917 (788 duplicated, 787 missing) | Observation sequence id | Excluded |
| Indication | category | Before patient contact; Before an aseptic procedure; After patient contact; After contact with patient Surroundings; After body fluid exposure | WHO hand hygiene moment | Allowed |
| HHaction | category | HW (hand wash), HR (hand rub), empty | Action performed; empty exactly when not compliant | Excluded (leakage) |
| Missedbutglove | category | Yes, No, empty | Missed opportunity but gloves worn; empty exactly when compliant | Excluded (leakage) |
| Complied | category | Yes, No | Target: hand hygiene performed at the opportunity | Target |

Derived: `complied` = 1 if Complied == "Yes" else 0.
Unconfirmed: exact definition of Missedbutglove should be checked against the original SAV codebook.
