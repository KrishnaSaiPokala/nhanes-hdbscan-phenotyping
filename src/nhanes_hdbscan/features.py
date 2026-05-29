"""Cardiometabolic feature-engineering utilities."""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd

from nhanes_hdbscan.config import FEATURE_BLOCKS


def safe_log1p(series: pd.Series) -> pd.Series:
    """Apply log1p after clipping negative values to missing."""
    values = pd.to_numeric(series, errors="coerce").astype(float)
    values = values.mask(values < 0)
    return np.log1p(values)


def add_log_features(frame: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    """Add ``log1p_<column>`` features for available skewed biomarkers."""
    out = frame.copy()
    for column in columns:
        if column in out.columns:
            out[f"log1p_{column}"] = safe_log1p(out[column])
    return out


def add_mean_blood_pressure(
    frame: pd.DataFrame,
    sbp_columns: Iterable[str],
    dbp_columns: Iterable[str],
) -> pd.DataFrame:
    """Add row-level mean systolic and diastolic blood-pressure features."""
    out = frame.copy()
    sbp_available = [col for col in sbp_columns if col in out.columns]
    dbp_available = [col for col in dbp_columns if col in out.columns]
    if sbp_available:
        out["mean_sbp"] = out[sbp_available].apply(pd.to_numeric, errors="coerce").mean(axis=1)
    if dbp_available:
        out["mean_dbp"] = out[dbp_available].apply(pd.to_numeric, errors="coerce").mean(axis=1)
    return out


def select_available_features(frame: pd.DataFrame, requested: Iterable[str]) -> list[str]:
    """Return requested feature names that are present in ``frame``."""
    return [column for column in requested if column in frame.columns]


def feature_blocks_for_available_columns(frame: pd.DataFrame) -> dict[str, list[str]]:
    """Return configured feature blocks restricted to available columns."""
    return {
        block: [column for column in columns if column in frame.columns]
        for block, columns in FEATURE_BLOCKS.items()
    }
