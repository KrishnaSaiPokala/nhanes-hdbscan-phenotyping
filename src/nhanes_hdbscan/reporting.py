"""Markdown report generation for portfolio and manuscript scaffolds."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from nhanes_hdbscan.config import PHENOTYPE_NAMES, PortfolioConfig
from nhanes_hdbscan.results import (
    ablation_summary,
    disease_enrichment,
    key_metrics,
    phenotype_profiles,
    replication_matches,
)


def pct(x: float, digits: int = 1) -> str:
    return f"{100 * float(x):.{digits}f}%"


def num(x: float, digits: int = 3) -> str:
    return f"{float(x):.{digits}f}"


def portfolio_markdown(data: dict[str, Any], figure_paths: list[Path]) -> str:
    m = key_metrics(data)
    profiles = phenotype_profiles(data)
    enrich = disease_enrichment(data).sort_values("lift_vs_overall", ascending=False)
    replication = replication_matches(data)

    lines = [
        "# NHANES-HDBSCAN Cardiometabolic Phenotyping",
        "",
        "Recruiter-facing, reproducible research software project for unsupervised cardiometabolic biomarker phenotyping in U.S. adults using public NHANES data.",
        "",
        "## Headline result",
        "",
        f"- Discovery cohort: **{m['n']:,} adults**",
        f"- Final solution: **{m['n_clusters']} HDBSCAN clusters plus a noise/outlier group**",
        f"- Mean noise rate: **{pct(m['noise_rate'], 2)}**",
        f"- Mean pairwise ARI: **{num(m['ari'], 4)}**",
        f"- Mean pairwise NMI: **{num(m['nmi'], 4)}**",
        f"- Mean non-noise silhouette: **{num(m['silhouette'], 4)}**",
        "",
        "## Why this is portfolio-grade",
        "",
        "This repository demonstrates a complete applied ML/research workflow: public data, clinical feature engineering, unsupervised representation learning, density-based clustering, multi-seed stability analysis, feature-block ablations, temporal replication, post-hoc disease-burden characterization, and manuscript-style reporting.",
        "",
        "Disease labels, survey weights, and demographic/socioeconomic variables are not used to create the primary clusters. They are used only after clustering for interpretation and enrichment.",
        "",
        "## Final selected model",
        "",
        f"- HDBSCAN `min_cluster_size`: **{m['min_cluster_size']}**",
        f"- HDBSCAN `min_samples`: **{m['min_samples']}**",
        f"- SVD components requested: **{m['svd_components']}**",
        f"- UMAP components: **{m['umap_components']}**",
        f"- UMAP neighbors: **{m['umap_neighbors']}**",
        "",
        "## Phenotype summary",
        "",
        "| Label | Interpretation | N | Percent | Technical drivers |",
        "|---:|---|---:|---:|---|",
    ]

    for row in profiles.itertuples(index=False):
        label = int(row.label)
        name = PHENOTYPE_NAMES.get(label, row.display_name)
        drivers = str(row.top_standardized_drivers).replace("|", "/")
        lines.append(f"| {label} | {name} | {int(row.n):,} | {pct(row.percent)} | {drivers} |")

    lines += [
        "",
        "## Strongest post-hoc enrichment signals",
        "",
        "| Phenotype | Outcome | Weighted prevalence/mean | Overall | Lift |",
        "|---|---|---:|---:|---:|",
    ]

    for row in enrich.head(12).itertuples(index=False):
        lines.append(
            f"| {row.display_name} | {row.outcome} | {num(row.weighted_mean_or_prevalence)} | "
            f"{num(row.overall_weighted_mean_or_prevalence)} | {num(row.lift_vs_overall, 2)} |"
        )

    lines += [
        "",
        "## Temporal replication",
        "",
        "| Discovery phenotype | Best replication phenotype | Profile correlation | Distance |",
        "|---:|---:|---:|---:|",
    ]

    for row in replication.itertuples(index=False):
        lines.append(
            f"| {int(row.discovery_label)} | {int(row.replication_label)} | "
            f"{num(row.profile_correlation, 3)} | {num(row.profile_euclidean_distance, 3)} |"
        )

    lines += ["", "## Generated figures", ""]
    for p in figure_paths:
        lines.append(f"- `{p.as_posix()}`")

    lines += [
        "",
        "## Claim discipline",
        "",
        "These findings should be framed as stable exploratory biomarker-derived phenotypes. They are not diagnostic classes, causal subtypes, or a clinical decision tool.",
        "",
    ]
    return "\n".join(lines)


def manuscript_results_scaffold(data: dict[str, Any]) -> str:
    m = key_metrics(data)
    profiles = phenotype_profiles(data)
    replication = replication_matches(data)
    ablations = ablation_summary(data)

    lines = [
        "# Manuscript Results Scaffold",
        "",
        "## Clustering solution and stability",
        "",
        f"The final discovery analysis included {m['n']:,} adults and identified {m['n_clusters']} non-noise HDBSCAN phenotypes plus an algorithmic noise/outlier group. Across final seeds, the mean pairwise ARI was {m['ari']:.4f} and the mean pairwise NMI was {m['nmi']:.4f}. The mean noise rate was {100 * m['noise_rate']:.2f}%.",
        "",
        "## Phenotype characterization",
        "",
    ]

    for row in profiles.itertuples(index=False):
        label = int(row.label)
        name = PHENOTYPE_NAMES.get(label, row.display_name)
        lines.append(
            f"Phenotype {label} ({name}) included {int(row.n):,} participants "
            f"({100 * float(row.percent):.1f}% of the analytic cohort). "
            f"Top standardized drivers were: {row.top_standardized_drivers}."
        )

    if "ARI_vs_full_reference_mean" in ablations.columns:
        lines += [
            "",
            "## Ablation robustness",
            "",
            "Feature-block ablations evaluated whether the solution depended disproportionately on a single biomarker block. The exported ablation table reports cluster count, noise rate, silhouette, and ARI versus the full objective reference solution.",
        ]

    if not replication.empty:
        lines += [
            "",
            "## Temporal replication",
            "",
            f"Best-match profile correlations in the pre-pandemic replication analysis ranged from {replication['profile_correlation'].min():.3f} to {replication['profile_correlation'].max():.3f}, supporting partial temporal transportability of the phenotype structure.",
        ]

    lines += [
        "",
        "## Interpretation boundary",
        "",
        "This study should be interpreted as exploratory unsupervised phenotyping. Post-hoc enrichment is descriptive and should not be interpreted causally.",
        "",
    ]
    return "\n".join(lines)


def write_reports(data: dict[str, Any], cfg: PortfolioConfig, figure_paths: list[Path]) -> list[Path]:
    cfg.docs_dir.mkdir(parents=True, exist_ok=True)
    cfg.manuscript_dir.mkdir(parents=True, exist_ok=True)
    cfg.summary_dir.mkdir(parents=True, exist_ok=True)
    portfolio = cfg.docs_dir / "portfolio_results_summary.md"
    manuscript = cfg.manuscript_dir / "results_scaffold.md"
    technical = cfg.summary_dir / "technical_summary.md"
    text = portfolio_markdown(data, figure_paths)
    portfolio.write_text(text, encoding="utf-8")
    manuscript.write_text(manuscript_results_scaffold(data), encoding="utf-8")
    technical.write_text(text, encoding="utf-8")
    return [portfolio, manuscript, technical]
