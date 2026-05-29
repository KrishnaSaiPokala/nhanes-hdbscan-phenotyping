"""Post-hoc phenotype enrichment utilities."""

from __future__ import annotations

import numpy as np
import pandas as pd


def weighted_mean(values: pd.Series, weights: pd.Series | None = None) -> float:
    """Return a weighted mean while ignoring missing values."""
    values = pd.to_numeric(values, errors="coerce")
    valid = values.notna()
    if weights is None:
        return float(values[valid].mean())
    weights = pd.to_numeric(weights, errors="coerce")
    valid &= weights.notna() & (weights > 0)
    if not valid.any():
        return float("nan")
    return float(np.average(values[valid], weights=weights[valid]))


def enrichment_by_group(
    frame: pd.DataFrame,
    group_col: str,
    outcome_col: str,
    weight_col: str | None = None,
) -> pd.DataFrame:
    """Compute group-wise weighted means and lift versus overall."""
    weights = frame[weight_col] if weight_col else None
    overall = weighted_mean(frame[outcome_col], weights)
    rows = []
    for group, subset in frame.groupby(group_col, dropna=False):
        subset_weights = subset[weight_col] if weight_col else None
        estimate = weighted_mean(subset[outcome_col], subset_weights)
        rows.append(
            {
                group_col: group,
                "outcome": outcome_col,
                "estimate": estimate,
                "overall": overall,
                "lift_vs_overall": estimate / overall if overall not in (0, np.nan) else np.nan,
            }
        )
    return pd.DataFrame(rows)
