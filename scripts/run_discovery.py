#!/usr/bin/env python3
"""Validate discovery configuration for local full-pipeline runs.

The public repository provides reusable pipeline components and aggregate
reporting outputs. Full raw-data execution requires locally downloaded NHANES
source files and environment-specific paths.
"""

from __future__ import annotations

from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nhanes_hdbscan.config import BIOMARKER_COLUMNS, FEATURE_BLOCKS


def main() -> int:
    """Print a discovery-run readiness summary."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("configs/discovery.yaml"))
    args = parser.parse_args()
    if not args.config.exists():
        raise FileNotFoundError(args.config)
    print(f"Discovery config: {args.config}")
    print(f"Configured biomarker count: {len(BIOMARKER_COLUMNS)}")
    print("Feature blocks:")
    for block, columns in FEATURE_BLOCKS.items():
        print(f"  - {block}: {', '.join(columns)}")
    print("Use scripts/make_research_report.py to reproduce committed aggregate outputs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
