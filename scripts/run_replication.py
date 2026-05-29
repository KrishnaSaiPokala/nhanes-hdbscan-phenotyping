#!/usr/bin/env python3
"""Validate replication configuration for local temporal-replication runs."""

from __future__ import annotations

from pathlib import Path
import argparse


def main() -> int:
    """Print a replication-run readiness summary."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("configs/replication.yaml"))
    args = parser.parse_args()
    if not args.config.exists():
        raise FileNotFoundError(args.config)
    print(f"Replication config: {args.config}")
    print("Replication matching is performed with phenotype profile correlations.")
    print("Use scripts/make_research_report.py to reproduce committed aggregate outputs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
