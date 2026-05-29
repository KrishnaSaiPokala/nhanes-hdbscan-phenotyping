# Reproducibility Notes

## Environment

The package targets Python 3.10 or newer. Install the base environment with:

```bash
python -m pip install -r requirements.txt
```

Optional end-to-end embedding and clustering dependencies are listed in `pyproject.toml` under the `full` extra.

## Aggregate-output reproduction

The committed aggregate report can be regenerated with:

```bash
python scripts/make_research_report.py
```

This command reads `results/summary/nhanes_hdbscan_results_v2_plus.json` and regenerates normalized tables, figures, the research summary, and the manuscript results scaffold.

## Raw data

Raw NHANES data files are not redistributed in this repository. Full raw-data execution requires users to download public NHANES source files and configure local paths.

## Quality checks

```bash
python -m black --check src scripts tests
python -m ruff check src scripts tests
python -m pytest -q
```
