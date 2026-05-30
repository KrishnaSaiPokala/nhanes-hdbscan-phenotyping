# Leakage-control design

The primary clustering feature space is restricted to objective examination and laboratory biomarkers.

## Used for primary clustering

- Age
- Body mass index and waist circumference
- Mean systolic and diastolic blood pressure
- HbA1c and glucose
- Triglycerides, HDL cholesterol, and LDL cholesterol
- eGFR and urinary albumin-to-creatinine ratio
- High-sensitivity C-reactive protein and white blood cell count

## Held out from primary clustering

- Disease labels
- Self-reported diagnoses
- Demographic variables
- Socioeconomic variables
- Survey weights
- Post-hoc burden outcomes

## Rationale

Holding these variables out reduces circularity. Disease-burden enrichment and demographic context are evaluated only after the biomarker-derived phenotype solution is frozen. Survey weights are not used to shape clustering geometry, but may be used for post-hoc weighted descriptive summaries.
