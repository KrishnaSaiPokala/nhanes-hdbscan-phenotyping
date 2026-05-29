# NHANES-HDBSCAN Cardiometabolic Phenotyping

Recruiter-facing, reproducible research software for unsupervised cardiometabolic biomarker phenotyping in U.S. adults using public NHANES data.

## Project identity

This project derives exploratory cardiometabolic biomarker phenotypes from objective NHANES examination and laboratory measurements using a density-based unsupervised learning workflow:

```text
NHANES biomarkers
→ cleaning and feature engineering
→ imputation and scaling
→ TruncatedSVD
→ UMAP representation learning
→ HDBSCAN density-based phenotyping
→ stability, ablation, replication, and enrichment analysis
```

The public portfolio repository emphasizes maintainable modular code, reproducible aggregate reporting, figures, and manuscript-ready summaries. Raw NHANES data are not redistributed.

## Generate the portfolio report

Place the aggregate result JSON at:

```bash
results/summary/nhanes_hdbscan_results_v2_plus.json
```

Then run:

```bash
python scripts/make_portfolio_report.py
```

Generated outputs:

- `figures/` — portfolio and manuscript figures
- `tables/` — normalized aggregate tables
- `docs/portfolio_results_summary.md` — recruiter-facing interpretation
- `manuscript/results_scaffold.md` — manuscript results starting point
- `results/summary/technical_summary.md` — technical summary

## Repository structure

```text
src/nhanes_hdbscan/     Modular research package
scripts/                Command-line entry points
configs/                Reproducible run configurations
figures/                Generated visual summaries
tables/                 Generated aggregate tables
docs/                   Portfolio documentation
manuscript/             Manuscript scaffolds
results/summary/        Small aggregate result exports only
```

## Claim discipline

This is an exploratory unsupervised phenotyping study. The clusters should be interpreted as stable biomarker-derived phenotypes, not diagnostic classes, causal subtypes, or a clinical decision tool.
