# Results audit summary

## Final selected model

- Discovery cohort: 6,048 adults
- SVD components requested: 75
- UMAP components: 10
- UMAP neighbors: 50
- HDBSCAN minimum cluster size: 300
- HDBSCAN minimum samples: 50
- Final non-noise phenotypes: 3
- Mean noise rate: 7.10%
- Mean non-noise silhouette: 0.9168
- Mean pairwise ARI: 0.9935
- Mean pairwise NMI: 0.9885

## Phenotype summary

| Phenotype | N | Percent | Interpretation |
|---|---:|---:|---|
| Algorithmic noise/outlier group | 447 | 7.4% | Observations not assigned to dense non-noise regions |
| Lipid-prediabetes metabolic-risk tendency | 2,998 | 49.6% | Descriptive lipid/prediabetes burden pattern |
| Lower-glycemic central-adiposity tendency | 2,258 | 37.3% | Central adiposity with comparatively lower glycemic burden |
| Higher blood-pressure/renal-risk tendency | 345 | 5.7% | Smaller dense region with BP and renal-risk signals |

## Main robustness finding

Feature-block ablation showed that removing lipid-domain variables was the most destabilizing perturbation, while most other single-domain removals preserved higher similarity to the full objective-biomarker reference solution.

## Temporal replication

Discovery-to-replication profile matching supported partial temporal profile transportability rather than exact phenotype identity. Best profile correlations ranged from 0.714 to 0.909.

## Triglycerides audit

The 2021-2023 triglycerides variable was resolved to `LBXTLG` from the alias set `LBXTLG; LBXTR; LBXSTR`. Missingness was 2,969 participants (49.1%). This is reported as a limitation and handled transparently in the supplement.
