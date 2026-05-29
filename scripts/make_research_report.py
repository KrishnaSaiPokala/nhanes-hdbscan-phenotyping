#!/usr/bin/env python3
"""Generate research tables, figures, and reports from aggregate results JSON."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nhanes_hdbscan.config import PortfolioConfig
from nhanes_hdbscan.reporting import write_reports
from nhanes_hdbscan.results import load_results_json, write_result_tables
from nhanes_hdbscan.visualization import make_all_figures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-json", type=Path, default=Path("results/summary/nhanes_hdbscan_results_v2_plus.json"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cfg = PortfolioConfig(results_json=args.results_json)
    data = load_results_json(cfg.results_json)

    table_paths = write_result_tables(data, cfg.tables_dir)
    figure_paths = make_all_figures(data, cfg)
    report_paths = write_reports(data, cfg, figure_paths)

    print("Generated tables:")
    for path in table_paths:
        print(f"  - {path}")
    print("Generated figures:")
    for path in figure_paths:
        print(f"  - {path}")
    print("Generated reports:")
    for path in report_paths:
        print(f"  - {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
