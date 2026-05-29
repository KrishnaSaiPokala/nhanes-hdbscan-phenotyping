"""Representation-learning helpers for SVD and UMAP embeddings."""

from __future__ import annotations

import numpy as np
from sklearn.decomposition import TruncatedSVD


def fit_svd(
    matrix: np.ndarray, n_components: int, random_state: int = 42
) -> tuple[np.ndarray, TruncatedSVD]:
    """Fit TruncatedSVD with a safe component count."""
    if matrix.ndim != 2:
        raise ValueError("matrix must be two-dimensional")
    max_components = max(1, min(n_components, matrix.shape[1] - 1, matrix.shape[0] - 1))
    model = TruncatedSVD(n_components=max_components, random_state=random_state)
    embedding = model.fit_transform(matrix)
    return np.asarray(embedding), model


def fit_umap(
    matrix: np.ndarray,
    n_neighbors: int = 50,
    n_components: int = 10,
    min_dist: float = 0.0,
    random_state: int = 42,
) -> tuple[np.ndarray, object]:
    """Fit UMAP when the optional dependency is installed."""
    try:
        from umap import UMAP
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise ImportError("Install the 'full' extra to use UMAP: pip install -e .[full]") from exc

    model = UMAP(
        n_neighbors=n_neighbors,
        n_components=n_components,
        min_dist=min_dist,
        metric="euclidean",
        random_state=random_state,
    )
    embedding = model.fit_transform(matrix)
    return np.asarray(embedding), model
