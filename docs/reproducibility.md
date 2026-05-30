# Reproducibility notes

## Minimal aggregate-report reproduction

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python scripts/make_research_report.py
python -m pytest -q
```

The aggregate-report workflow reads `results/summary/nhanes_hdbscan_results_v2_plus.json` and regenerates normalized reporting tables, figures, and manuscript-oriented summaries.

## Full local reconstruction

Full local reconstruction requires obtaining NHANES public-use files directly from NCHS/CDC. Raw source data are not redistributed here.

## Versioning recommendation

Use a tagged release such as `v1.0.0-preprint` for the medRxiv version. After medRxiv assigns a DOI, create a follow-up release with the DOI in the README and `CITATION.cff`.
