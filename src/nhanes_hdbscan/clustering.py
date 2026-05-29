"""Clustering helpers for HDBSCAN and comparator models."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


def fit_hdbscan(
    matrix: np.ndarray,
    min_cluster_size: int = 300,
    min_samples: int = 50,
    metric: str = "euclidean",
) -> tuple[np.ndarray, object]:
    """Fit HDBSCAN when the optional dependency is installed."""
    try:
        import hdbscan
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise ImportError(
            "Install the 'full' extra to use HDBSCAN: pip install -e .[full]"
        ) from exc

    model = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        metric=metric,
        prediction_data=True,
    )
    labels = model.fit_predict(matrix)
    return np.asarray(labels), model


def fit_kmeans(
    matrix: np.ndarray, n_clusters: int, random_state: int = 42
) -> tuple[np.ndarray, KMeans]:
    """Fit KMeans as a simple comparator clustering model."""
    model = KMeans(n_clusters=n_clusters, random_state=random_state, n_init="auto")
    labels = model.fit_predict(matrix)
    return np.asarray(labels), model


def cluster_summary(labels: np.ndarray) -> pd.DataFrame:
    """Return cluster sizes and proportions, preserving the HDBSCAN noise label."""
    labels = np.asarray(labels)
    values, counts = np.unique(labels, return_counts=True)
    total = counts.sum()
    return pd.DataFrame(
        {
            "label": values.astype(int),
            "n": counts.astype(int),
            "percent": counts / total if total else np.nan,
            "is_noise": values == -1,
        }
    ).sort_values(["is_noise", "label"])


def noise_rate(labels: np.ndarray) -> float:
    """Return the fraction of observations assigned to HDBSCAN noise."""
    labels = np.asarray(labels)
    if labels.size == 0:
        return float("nan")
    return float(np.mean(labels == -1))
