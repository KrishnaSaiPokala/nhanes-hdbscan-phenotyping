# NHANES-HDBSCAN Cardiometabolic Phenotyping

Recruiter-facing, reproducible research software project for unsupervised cardiometabolic biomarker phenotyping in U.S. adults using public NHANES data.

## Headline result

- Discovery cohort: **6,048 adults**
- Final solution: **3 HDBSCAN clusters plus a noise/outlier group**
- Mean noise rate: **7.10%**
- Mean pairwise ARI: **0.9935**
- Mean pairwise NMI: **0.9885**
- Mean non-noise silhouette: **0.9168**

## Why this is portfolio-grade

This repository demonstrates a complete applied ML/research workflow: public data, clinical feature engineering, unsupervised representation learning, density-based clustering, multi-seed stability analysis, feature-block ablations, temporal replication, post-hoc disease-burden characterization, and manuscript-style reporting.

Disease labels, survey weights, and demographic/socioeconomic variables are not used to create the primary clusters. They are used only after clustering for interpretation and enrichment.

## Final selected model

- HDBSCAN `min_cluster_size`: **300**
- HDBSCAN `min_samples`: **50**
- SVD components requested: **75**
- UMAP components: **10**
- UMAP neighbors: **50**

## Phenotype summary

| Label | Interpretation | N | Percent | Technical drivers |
|---:|---|---:|---:|---|
| -1 | Noise / outlier group | 447 | 7.4% | HDBSCAN noise label |
| 0 | Lipid-prediabetes metabolic-risk tendency | 2,998 | 49.6% | wbc z=-0.17; albumin z=-0.07; mean_sbp z=-0.06; mean_dbp z=-0.05 |
| 1 | Lower-glycemic central-adiposity tendency | 2,258 | 37.3% | wbc z=0.20; albumin z=0.11; glucose z=-0.07; mean_dbp z=0.05 |
| 2 | Smaller blood-pressure / renal-risk phenotype | 345 | 5.7% | mean_sbp z=0.18; wbc z=0.15; mean_dbp z=0.12; rdw z=0.12 |

## Strongest post-hoc enrichment signals

| Phenotype | Outcome | Weighted prevalence/mean | Overall | Lift |
|---|---|---:|---:|---:|
| Smaller blood-pressure / renal-risk phenotype | albuminuria | 0.160 | 0.101 | 1.58 |
| Lipid-prediabetes metabolic-risk tendency | prediabetes_biomarker | 0.499 | 0.370 | 1.35 |
| Smaller blood-pressure / renal-risk phenotype | diabetes_any | 0.179 | 0.149 | 1.20 |
| Smaller blood-pressure / renal-risk phenotype | cvd_self_report | 0.114 | 0.096 | 1.19 |
| Noise / outlier group | albuminuria | 0.117 | 0.101 | 1.15 |
| Lipid-prediabetes metabolic-risk tendency | metabolic_syndrome_count | 1.976 | 1.747 | 1.13 |
| Smaller blood-pressure / renal-risk phenotype | hypertension_any | 0.573 | 0.506 | 1.13 |
| Smaller blood-pressure / renal-risk phenotype | ckd_risk | 0.160 | 0.141 | 1.13 |
| Lipid-prediabetes metabolic-risk tendency | diabetes_any | 0.164 | 0.149 | 1.10 |
| Lower-glycemic central-adiposity tendency | central_obesity | 0.598 | 0.558 | 1.07 |
| Lipid-prediabetes metabolic-risk tendency | dyslipidemia | 0.590 | 0.552 | 1.07 |
| Noise / outlier group | cvd_self_report | 0.101 | 0.096 | 1.05 |

## Temporal replication

| Discovery phenotype | Best replication phenotype | Profile correlation | Distance |
|---:|---:|---:|---:|
| 0 | 3 | 0.861 | 0.121 |
| 1 | 1 | 0.909 | 0.208 |
| 2 | 1 | 0.714 | 0.208 |

## Generated figures

- `figures/pipeline_diagram.png`
- `figures/cluster_size_distribution.png`
- `figures/multi_seed_stability_metrics.png`
- `figures/seed_level_quality_metrics.png`
- `figures/phenotype_biomarker_heatmap.png`
- `figures/disease_enrichment_lift_heatmap.png`
- `figures/ablation_ari_vs_full_reference.png`
- `figures/replication_profile_correlations.png`

## Claim discipline

These findings should be framed as stable exploratory biomarker-derived phenotypes. They are not diagnostic classes, causal subtypes, or a clinical decision tool.
