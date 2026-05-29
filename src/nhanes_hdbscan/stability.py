"""Multi-run clustering stability utilities."""

from __future__ import annotations

from itertools import combinations

import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score


def pairwise_stability(label_runs: dict[str, np.ndarray]) -> pd.DataFrame:
    """Compute pairwise ARI and NMI across named clustering runs."""
    rows: list[dict[str, float | str]] = []
    for (name_a, labels_a), (name_b, labels_b) in combinations(label_runs.items(), 2):
        if len(labels_a) != len(labels_b):
            raise ValueError(f"Run length mismatch between {name_a!r} and {name_b!r}")
        rows.append(
            {
                "run_a": name_a,
                "run_b": name_b,
                "ari": adjusted_rand_score(labels_a, labels_b),
                "nmi": normalized_mutual_info_score(labels_a, labels_b),
            }
        )
    return pd.DataFrame(rows)


def summarize_stability(pairwise: pd.DataFrame) -> dict[str, float]:
    """Summarize pairwise stability diagnostics."""
    if pairwise.empty:
        return {"mean_pairwise_ARI": np.nan, "mean_pairwise_NMI": np.nan}
    return {
        "mean_pairwise_ARI": float(pairwise["ari"].mean()),
        "median_pairwise_ARI": float(pairwise["ari"].median()),
        "mean_pairwise_NMI": float(pairwise["nmi"].mean()),
        "median_pairwise_NMI": float(pairwise["nmi"].median()),
    }
