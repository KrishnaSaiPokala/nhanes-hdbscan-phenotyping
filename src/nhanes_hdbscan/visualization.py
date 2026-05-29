"""Research and manuscript figure generation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from nhanes_hdbscan.config import ResearchConfig
from nhanes_hdbscan.results import (
    ablation_summary,
    biomarker_z_matrix,
    disease_enrichment,
    final_seed_runs,
    phenotype_profiles,
    replication_matches,
)

plt.rcParams.update(
    {
        "figure.autolayout": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titleweight": "bold",
        "font.size": 10,
    }
)


def save(fig: plt.Figure, path: Path, dpi: int) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    return path


def annotate_bars(ax: plt.Axes, fmt: str) -> None:
    for patch in ax.patches:
        height = patch.get_height()
        if np.isfinite(height):
            ax.annotate(
                fmt.format(height),
                (patch.get_x() + patch.get_width() / 2, height),
                ha="center",
                va="bottom",
                fontsize=8,
                xytext=(0, 2),
                textcoords="offset points",
            )


def plot_pipeline(figures_dir: Path, cfg: ResearchConfig) -> Path:
    steps = [
        "Public NHANES\nXPT files",
        "Adult cohort\nobjective biomarkers",
        "Cleaning +\nfeature engineering",
        "Imputation +\nscaling",
        "TruncatedSVD",
        "UMAP\nembedding",
        "HDBSCAN\nphenotypes",
        "Stability, ablation,\nreplication, enrichment",
    ]
    fig, ax = plt.subplots(figsize=(12, 3.2))
    ax.axis("off")
    xs = np.linspace(0.05, 0.95, len(steps))
    for i, (x, label) in enumerate(zip(xs, steps)):
        ax.text(
            x,
            0.55,
            label,
            ha="center",
            va="center",
            fontsize=8,
            bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor="black"),
        )
        if i < len(steps) - 1:
            ax.annotate(
                "",
                xy=(xs[i + 1] - 0.045, 0.55),
                xytext=(x + 0.045, 0.55),
                arrowprops=dict(arrowstyle="->", lw=1.2),
            )
    ax.set_title("Reproducible NHANES-HDBSCAN phenotyping workflow")
    return save(fig, figures_dir / "pipeline_diagram.png", cfg.dpi)


def plot_cluster_sizes(data: dict[str, Any], figures_dir: Path, cfg: ResearchConfig) -> Path:
    df = phenotype_profiles(data)
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.bar(df["display_name"], df["n"])
    ax.set_title("Final HDBSCAN phenotype sizes")
    ax.set_ylabel("Participants")
    ax.tick_params(axis="x", rotation=25, labelsize=8)
    annotate_bars(ax, "{:.0f}")
    return save(fig, figures_dir / "cluster_size_distribution.png", cfg.dpi)


def plot_stability(data: dict[str, Any], figures_dir: Path, cfg: ResearchConfig) -> Path:
    s = data["stability"]
    vals = {
        "Mean ARI": s["mean_pairwise_ARI"],
        "Median ARI": s["median_pairwise_ARI"],
        "Mean NMI": s["mean_pairwise_NMI"],
        "Median NMI": s["median_pairwise_NMI"],
    }
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.bar(list(vals.keys()), list(vals.values()))
    ax.set_ylim(0, 1.05)
    ax.set_title("Multi-seed clustering stability")
    ax.set_ylabel("Agreement")
    annotate_bars(ax, "{:.3f}")
    return save(fig, figures_dir / "multi_seed_stability_metrics.png", cfg.dpi)


def plot_seed_quality(data: dict[str, Any], figures_dir: Path, cfg: ResearchConfig) -> Path:
    df = final_seed_runs(data)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df["seed"].astype(str), df["noise_rate"], marker="o", label="Noise rate")
    ax.plot(df["seed"].astype(str), df["silhouette_non_noise"], marker="o", label="Silhouette")
    ax.set_title("Seed-level quality metrics")
    ax.set_xlabel("Seed")
    ax.set_ylabel("Metric value")
    ax.legend(frameon=False)
    return save(fig, figures_dir / "seed_level_quality_metrics.png", cfg.dpi)


def plot_biomarker_heatmap(data: dict[str, Any], figures_dir: Path, cfg: ResearchConfig) -> Path:
    mat = biomarker_z_matrix(data)
    fig, ax = plt.subplots(figsize=(13, 7))
    im = ax.imshow(mat.to_numpy(dtype=float), aspect="auto", cmap="coolwarm", vmin=-2, vmax=2)
    ax.set_xticks(np.arange(mat.shape[1]))
    ax.set_xticklabels(mat.columns, rotation=35, ha="right")
    ax.set_yticks(np.arange(mat.shape[0]))
    ax.set_yticklabels(mat.index)
    ax.set_title("Relative biomarker profile by phenotype")
    cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    cbar.set_label("Within-biomarker z-score")
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            val = mat.iloc[i, j]
            ax.text(
                j, i, "NA" if pd.isna(val) else f"{val:.1f}", ha="center", va="center", fontsize=7
            )
    return save(fig, figures_dir / "phenotype_biomarker_heatmap.png", cfg.dpi)


def plot_disease_lift(data: dict[str, Any], figures_dir: Path, cfg: ResearchConfig) -> Path:
    df = disease_enrichment(data)
    pivot = df.pivot_table(
        index="outcome", columns="display_name", values="lift_vs_overall", aggfunc="mean"
    ).sort_index()
    fig, ax = plt.subplots(figsize=(13, 8))
    im = ax.imshow(pivot.to_numpy(dtype=float), aspect="auto", cmap="RdBu_r", vmin=0.5, vmax=1.5)
    ax.set_xticks(np.arange(pivot.shape[1]))
    ax.set_xticklabels(pivot.columns, rotation=30, ha="right")
    ax.set_yticks(np.arange(pivot.shape[0]))
    ax.set_yticklabels(pivot.index)
    ax.set_title("Post-hoc disease-burden lift vs overall")
    cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    cbar.set_label("Lift vs overall")
    for i in range(pivot.shape[0]):
        for j in range(pivot.shape[1]):
            val = pivot.iloc[i, j]
            ax.text(
                j, i, "NA" if pd.isna(val) else f"{val:.2f}", ha="center", va="center", fontsize=7
            )
    return save(fig, figures_dir / "disease_enrichment_lift_heatmap.png", cfg.dpi)


def plot_ablation(data: dict[str, Any], figures_dir: Path, cfg: ResearchConfig) -> Path:
    df = ablation_summary(data)
    fig, ax = plt.subplots(figsize=(11, 7))
    col = "ARI_vs_full_reference_mean"
    if col in df.columns:
        ordered = df.sort_values(col)
        ax.barh(ordered["ablation"], ordered[col])
        ax.set_xlim(0, 1.05)
        ax.set_xlabel("ARI vs full objective reference")
        ax.set_title("Feature-block ablation robustness")
    else:
        ax.text(0.5, 0.5, "No ARI ablation metric available", ha="center", va="center")
    return save(fig, figures_dir / "ablation_ari_vs_full_reference.png", cfg.dpi)


def plot_replication(data: dict[str, Any], figures_dir: Path, cfg: ResearchConfig) -> Path:
    df = replication_matches(data)
    labels = [f"D{int(r.discovery_label)} → R{int(r.replication_label)}" for r in df.itertuples()]
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.bar(labels, df["profile_correlation"])
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Profile correlation")
    ax.set_title("Best temporal-replication phenotype matches")
    annotate_bars(ax, "{:.2f}")
    return save(fig, figures_dir / "replication_profile_correlations.png", cfg.dpi)


def make_all_figures(data: dict[str, Any], cfg: ResearchConfig) -> list[Path]:
    cfg.figures_dir.mkdir(parents=True, exist_ok=True)
    return [
        plot_pipeline(cfg.figures_dir, cfg),
        plot_cluster_sizes(data, cfg.figures_dir, cfg),
        plot_stability(data, cfg.figures_dir, cfg),
        plot_seed_quality(data, cfg.figures_dir, cfg),
        plot_biomarker_heatmap(data, cfg.figures_dir, cfg),
        plot_disease_lift(data, cfg.figures_dir, cfg),
        plot_ablation(data, cfg.figures_dir, cfg),
        plot_replication(data, cfg.figures_dir, cfg),
    ]
