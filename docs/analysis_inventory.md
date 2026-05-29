# Analysis Inventory

This document summarizes the committed aggregate outputs and reproducibility artifacts in the repository.

## Final model configuration

| Parameter | Value |
|---|---:|
| HDBSCAN `min_cluster_size` | 300 |
| HDBSCAN `min_samples` | 50 |
| SVD components requested | 75 |
| UMAP components | 10 |
| UMAP neighbors | 50 |

## Stability and quality

| Metric | Value |
|---|---:|
| Mean pairwise ARI | 0.9935 |
| Median pairwise ARI | 0.9932 |
| Mean pairwise NMI | 0.9885 |
| Median pairwise NMI | 0.9836 |
| Mean non-noise silhouette | 0.9168 |
| Mean noise rate | 7.10% |

## Phenotype counts

| Label | Name | N | Percent |
|---:|---|---:|---:|
| -1 | algorithmic_noise_outlier_group | 447 | 7.4% |
| 0 | phenotype_0__low_wbc__low_albumin__low_mean_sbp | 2,998 | 49.6% |
| 1 | phenotype_1__high_wbc__high_albumin__low_glucose | 2,258 | 37.3% |
| 2 | phenotype_2__high_mean_sbp__high_wbc__high_mean_dbp | 345 | 5.7% |

## Committed figures

- `figures/pipeline_diagram.png`
- `figures/cluster_size_distribution.png`
- `figures/multi_seed_stability_metrics.png`
- `figures/seed_level_quality_metrics.png`
- `figures/phenotype_biomarker_heatmap.png`
- `figures/disease_enrichment_lift_heatmap.png`
- `figures/ablation_ari_vs_full_reference.png`
- `figures/replication_profile_correlations.png`

## Committed tables

- `tables/phenotype_profiles.csv`
- `tables/disease_enrichment.csv`
- `tables/final_seed_runs.csv`
- `tables/ablation_summary.csv`
- `tables/replication_matches.csv`

## Interpretation boundary

These outputs support exploratory phenotype characterization and research reporting. They do not establish causal relationships, clinical diagnostic groups, or treatment recommendations.
