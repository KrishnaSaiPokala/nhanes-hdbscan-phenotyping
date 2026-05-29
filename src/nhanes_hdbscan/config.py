"""Project configuration and constants."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

PROJECT_SHORT_NAME = "NHANES-HDBSCAN Cardiometabolic Phenotyping"
PROJECT_TITLE = "Stable Density-Based Cardiometabolic Phenotypes in U.S. Adults"

PHENOTYPE_NAMES = {
    -1: "Noise / outlier group",
    0: "Lipid-prediabetes metabolic-risk tendency",
    1: "Lower-glycemic central-adiposity tendency",
    2: "Smaller blood-pressure / renal-risk phenotype",
}

BIOMARKER_COLUMNS = [
    "age_mean", "bmi_mean", "waist_cm_mean", "mean_sbp_mean", "mean_dbp_mean",
    "hba1c_mean", "glucose_mean", "triglycerides_mean", "hdl_mean", "ldl_mean",
    "egfr_mean", "uacr_mean", "hscrp_mean", "wbc_mean",
]

BIOMARKER_DISPLAY = {
    "age_mean": "Age",
    "bmi_mean": "BMI",
    "waist_cm_mean": "Waist",
    "mean_sbp_mean": "SBP",
    "mean_dbp_mean": "DBP",
    "hba1c_mean": "HbA1c",
    "glucose_mean": "Glucose",
    "triglycerides_mean": "Triglycerides",
    "hdl_mean": "HDL",
    "ldl_mean": "LDL",
    "egfr_mean": "eGFR",
    "uacr_mean": "UACR",
    "hscrp_mean": "hs-CRP",
    "wbc_mean": "WBC",
}

@dataclass(frozen=True)
class PortfolioConfig:
    """Filesystem configuration for report generation."""

    results_json: Path = Path("results/summary/nhanes_hdbscan_results_v2_plus.json")
    figures_dir: Path = Path("figures")
    tables_dir: Path = Path("tables")
    docs_dir: Path = Path("docs")
    manuscript_dir: Path = Path("manuscript")
    summary_dir: Path = Path("results/summary")
    dpi: int = 220
