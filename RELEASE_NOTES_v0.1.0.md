# v0.1.0 — Initial reproducible research software release

Initial release of the NHANES-HDBSCAN cardiometabolic phenotyping research-software repository.

## Included

- Modular utilities for data access, cleaning, feature engineering, preprocessing, embedding, clustering, stability, ablation, enrichment, replication, visualization, and reporting.
- Aggregate-result validation and normalized table export.
- Manuscript-ready figures and research-results summaries generated from final aggregate outputs.
- Unit tests, Ruff linting, Black formatting, Makefile commands, CI workflow, citation metadata, and MIT license.

## Headline aggregate results

- Discovery cohort: 6,048 adults.
- Final HDBSCAN solution: 3 non-noise phenotypes plus an algorithmic noise/outlier group.
- Mean pairwise ARI: 0.9935.
- Mean pairwise NMI: 0.9885.
- Mean noise rate: 7.10%.

## Scientific boundary

The repository supports exploratory unsupervised phenotyping and reproducible aggregate reporting. It does not provide diagnostic classes, causal claims, treatment recommendations, or a clinical decision tool.
