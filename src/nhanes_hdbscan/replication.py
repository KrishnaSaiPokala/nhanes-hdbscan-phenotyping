"""Temporal replication and profile-matching utilities."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist


def match_profiles_by_correlation(
    discovery_profiles: pd.DataFrame,
    replication_profiles: pd.DataFrame,
    feature_columns: list[str],
    discovery_label_col: str = "label",
    replication_label_col: str = "label",
) -> pd.DataFrame:
    """Match discovery phenotypes to replication phenotypes by profile correlation."""
    discovery = discovery_profiles[feature_columns].to_numpy(dtype=float)
    replication = replication_profiles[feature_columns].to_numpy(dtype=float)
    distance = cdist(discovery, replication, metric="correlation")

    rows = []
    for i, row in discovery_profiles.reset_index(drop=True).iterrows():
        best_j = int(np.nanargmin(distance[i]))
        rows.append(
            {
                "discovery_label": row[discovery_label_col],
                "replication_label": replication_profiles.reset_index(drop=True).loc[
                    best_j, replication_label_col
                ],
                "profile_correlation": 1 - float(distance[i, best_j]),
                "profile_correlation_distance": float(distance[i, best_j]),
            }
        )
    return pd.DataFrame(rows)
