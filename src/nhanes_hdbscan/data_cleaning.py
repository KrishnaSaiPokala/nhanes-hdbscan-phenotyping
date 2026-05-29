"""Data-cleaning helpers for tabular NHANES-derived data."""

from __future__ import annotations

import re
from collections.abc import Iterable

import numpy as np
import pandas as pd


def normalize_column_names(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with snake_case column names."""
    renamed = {
        column: re.sub(r"_+", "_", re.sub(r"[^0-9a-zA-Z]+", "_", str(column)).strip("_").lower())
        for column in frame.columns
    }
    return frame.rename(columns=renamed).copy()


def coerce_numeric(frame: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    """Coerce selected columns to numeric values while preserving other columns."""
    out = frame.copy()
    for column in columns:
        if column in out.columns:
            out[column] = pd.to_numeric(out[column], errors="coerce")
    return out


def missingness_report(frame: pd.DataFrame) -> pd.DataFrame:
    """Return missing-count and missing-rate diagnostics by column."""
    total = len(frame)
    missing = frame.isna().sum().rename("missing_n")
    report = missing.to_frame()
    report["missing_rate"] = np.where(total > 0, report["missing_n"] / total, np.nan)
    report["non_missing_n"] = total - report["missing_n"]
    return report.reset_index(names="column").sort_values("missing_rate", ascending=False)


def drop_sparse_columns(frame: pd.DataFrame, max_missing_rate: float) -> pd.DataFrame:
    """Drop columns whose missingness exceeds ``max_missing_rate``."""
    if not 0 <= max_missing_rate <= 1:
        raise ValueError("max_missing_rate must be between 0 and 1")
    keep = frame.isna().mean() <= max_missing_rate
    return frame.loc[:, keep].copy()
