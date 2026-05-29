"""Load, validate, and normalize aggregate NHANES-HDBSCAN results."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from nhanes_hdbscan.config import BIOMARKER_COLUMNS, BIOMARKER_DISPLAY, PHENOTYPE_NAMES

REQUIRED_KEYS = {
    "project", "final_selected_params", "selection_row", "stability", "final_seed_rows",
    "phenotype_profiles", "disease_enrichment", "ablation_summary", "best_replication_matches",
}


def load_results_json(path: str | Path) -> dict[str, Any]:
    """Load the final aggregate JSON exported from the research run."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Missing results JSON: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    missing = sorted(REQUIRED_KEYS - set(data))
    if missing:
        raise ValueError(f"Results JSON missing required keys: {missing}")
    return data


def phenotype_profiles(data: dict[str, Any]) -> pd.DataFrame:
    """Return phenotype profile table with human-readable names."""
    df = pd.DataFrame(data["phenotype_profiles"]).copy()
    df["label"] = df["label"].astype(int)
    df["display_name"] = df["label"].map(PHENOTYPE_NAMES).fillna(df.get("phenotype_name", ""))
    return df.sort_values("label")


def disease_enrichment(data: dict[str, Any]) -> pd.DataFrame:
    """Return post-hoc disease enrichment table."""
    df = pd.DataFrame(data["disease_enrichment"]).copy()
    df["label"] = df["label"].astype(int)
    df["display_name"] = df["label"].map(PHENOTYPE_NAMES).fillna(df["label"].astype(str))
    return df.sort_values(["outcome", "label"])


def final_seed_runs(data: dict[str, Any]) -> pd.DataFrame:
    """Return seed-level final model diagnostics."""
    return pd.DataFrame(data["final_seed_rows"])


def replication_matches(data: dict[str, Any]) -> pd.DataFrame:
    """Return best discovery-to-replication phenotype matches."""
    return pd.DataFrame(data["best_replication_matches"]).sort_values("discovery_label")


def parse_ablation_key(raw: str) -> tuple[str, str]:
    """Parse serialized tuple keys such as ('noise_rate', 'mean')."""
    cleaned = raw.replace("(", "").replace(")", "").replace("'", "").replace('"', "")
    parts = [part.strip() for part in cleaned.split(",") if part.strip()]
    if len(parts) >= 2:
        return parts[0], parts[1]
    return cleaned, "value"


def ablation_summary(data: dict[str, Any]) -> pd.DataFrame:
    """Flatten ablation summary dictionary into a tidy table."""
    rows: dict[str, dict[str, Any]] = {}
    for raw_key, values in data["ablation_summary"].items():
        metric, stat = parse_ablation_key(raw_key)
        if not isinstance(values, dict):
            continue
        for ablation_name, value in values.items():
            rows.setdefault(ablation_name, {"ablation": ablation_name})
            rows[ablation_name][f"{metric}_{stat}"] = value
    return pd.DataFrame(rows.values()).sort_values("ablation")


def biomarker_z_matrix(data: dict[str, Any]) -> pd.DataFrame:
    """Create a phenotype-by-biomarker z-score matrix for heatmaps."""
    profiles = phenotype_profiles(data)
    available = [col for col in BIOMARKER_COLUMNS if col in profiles.columns]
    matrix = profiles.set_index("display_name")[available].apply(pd.to_numeric, errors="coerce")
    z = matrix.copy()
    for column in z.columns:
        sd = z[column].std(skipna=True, ddof=0)
        if sd and np.isfinite(sd):
            z[column] = (z[column] - z[column].mean(skipna=True)) / sd
        else:
            z[column] = np.nan
    return z.rename(columns=BIOMARKER_DISPLAY)


def key_metrics(data: dict[str, Any]) -> dict[str, Any]:
    """Return headline metrics used in README/report text."""
    profiles = phenotype_profiles(data)
    selection = data["selection_row"]
    stability = data["stability"]
    params = data["final_selected_params"]
    return {
        "n": int(profiles["n"].sum()),
        "n_clusters": int(selection["mean_n_clusters"]),
        "noise_rate": float(selection["mean_noise_rate"]),
        "silhouette": float(selection["mean_silhouette"]),
        "ari": float(stability["mean_pairwise_ARI"]),
        "nmi": float(stability["mean_pairwise_NMI"]),
        "min_cluster_size": int(params["min_cluster_size"]),
        "min_samples": int(params["min_samples"]),
        "svd_components": int(params["svd_components"]),
        "umap_components": int(params["umap_components"]),
        "umap_neighbors": int(params["umap_neighbors"]),
        "takeaway": data.get("plain_english_takeaway", ""),
    }


def write_result_tables(data: dict[str, Any], output_dir: str | Path) -> list[Path]:
    """Write normalized CSV tables for GitHub and manuscript use."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    tables = {
        "phenotype_profiles.csv": phenotype_profiles(data),
        "disease_enrichment.csv": disease_enrichment(data),
        "final_seed_runs.csv": final_seed_runs(data),
        "ablation_summary.csv": ablation_summary(data),
        "replication_matches.csv": replication_matches(data),
    }
    paths: list[Path] = []
    for filename, frame in tables.items():
        path = output_dir / filename
        frame.to_csv(path, index=False)
        paths.append(path)
    return paths
