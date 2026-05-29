import numpy as np
import pandas as pd

from nhanes_hdbscan.ablations import leave_one_block_out_feature_sets
from nhanes_hdbscan.clustering import cluster_summary, noise_rate
from nhanes_hdbscan.data_cleaning import missingness_report, normalize_column_names
from nhanes_hdbscan.enrichment import enrichment_by_group, weighted_mean
from nhanes_hdbscan.features import safe_log1p, select_available_features
from nhanes_hdbscan.preprocessing import fit_transform_biomarkers
from nhanes_hdbscan.stability import pairwise_stability, summarize_stability


def test_cleaning_and_feature_helpers():
    frame = pd.DataFrame({"A Value": [1, None], "Triglycerides": [10, -1]})
    clean = normalize_column_names(frame)
    assert list(clean.columns) == ["a_value", "triglycerides"]
    report = missingness_report(clean)
    assert {"column", "missing_n", "missing_rate"}.issubset(report.columns)
    logged = safe_log1p(clean["triglycerides"])
    assert np.isfinite(logged.iloc[0])
    assert np.isnan(logged.iloc[1])
    assert select_available_features(clean, ["a_value", "missing"]) == ["a_value"]


def test_preprocessing_and_ablation_helpers():
    frame = pd.DataFrame({"x": [1, 2, None], "y": [2, 4, 6]})
    result = fit_transform_biomarkers(frame, ["x", "y"])
    assert result.matrix.shape == (3, 2)
    ablations = leave_one_block_out_feature_sets({"a": ["x"], "b": ["y"]})
    assert ablations["full"] == ["x", "y"]
    assert ablations["drop_a"] == ["y"]


def test_clustering_stability_and_enrichment_helpers():
    labels = np.array([-1, 0, 0, 1])
    summary = cluster_summary(labels)
    assert int(summary["n"].sum()) == 4
    assert noise_rate(labels) == 0.25

    pairwise = pairwise_stability({"a": labels, "b": labels.copy()})
    stats = summarize_stability(pairwise)
    assert stats["mean_pairwise_ARI"] == 1.0
    assert stats["mean_pairwise_NMI"] == 1.0

    frame = pd.DataFrame({"group": [0, 0, 1], "outcome": [1, 0, 1], "weight": [1, 1, 2]})
    assert weighted_mean(frame["outcome"], frame["weight"]) == 0.75
    enrich = enrichment_by_group(frame, "group", "outcome", "weight")
    assert {"estimate", "overall", "lift_vs_overall"}.issubset(enrich.columns)
