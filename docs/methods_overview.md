# Methods Overview

This repository implements modular utilities for a density-based cardiometabolic phenotyping workflow using public NHANES data.

## Primary clustering inputs

The primary feature space uses objective cardiometabolic biomarkers and excludes disease labels, demographic variables, socioeconomic variables, and survey weights from cluster formation.

## Representation and clustering

The workflow combines imputation and scaling, TruncatedSVD, UMAP embedding, and HDBSCAN density-based clustering. Comparator and helper utilities are included for local extensions.

## Validation layers

The committed aggregate outputs include:

- multi-seed stability diagnostics,
- feature-block ablation summaries,
- post-hoc disease-burden enrichment,
- temporal phenotype-profile matching,
- manuscript-oriented figures and tables.

## Interpretation

Phenotype labels are descriptive and exploratory. They should not be interpreted as diagnoses, causal subtypes, or clinical decision rules.
