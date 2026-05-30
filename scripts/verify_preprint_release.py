#!/usr/bin/env python3
"""Lightweight repository-state checks for the medRxiv preprint release."""
from __future__ import annotations

from pathlib import Path
import sys

REQUIRED = [
    "README.md",
    "CITATION.cff",
    "preprint/medrxiv/v1/Pokala_NHANES_HDBSCAN_Manuscript.pdf",
    "preprint/medrxiv/v1/Pokala_NHANES_HDBSCAN_Supplementary_Material.pdf",
    "figures/main/figure1_study_design_leakage_control.png",
    "figures/main/figure2_phenotype_solution_stability.png",
    "figures/main/figure3_biomarker_phenotype_atlas.png",
    "figures/main/figure4_posthoc_burden_gradients.png",
    "figures/main/figure5_robustness_temporal_transportability.png",
    "tables/curated/table1_final_phenotype_groups_curated.csv",
    "tables/curated/table2_selected_posthoc_enrichment_curated.csv",
    "tables/curated/table3_model_stability_audit_curated.csv",
    "results/summary/nhanes_hdbscan_results_v2_plus.json",
    "docs/data_availability.md",
    "docs/leakage_control.md",
    "docs/results_audit.md",
    "docs/known_limitations.md",
    "docs/reproducibility.md",
]


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    missing = [p for p in REQUIRED if not (root / p).exists()]
    if missing:
        print("Missing required release files:")
        for path in missing:
            print(f"  - {path}")
        return 1
    print("Repository preprint-release file check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
