"""Preprocessing utilities for biomarker matrices."""

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Iterable

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


@dataclass(frozen=True)
class PreprocessedMatrix:
    """Container for a fitted biomarker matrix and its preprocessing pipeline."""

    matrix: np.ndarray
    feature_names: list[str]
    pipeline: Pipeline


def build_preprocessing_pipeline() -> Pipeline:
    """Return median-imputation plus z-score scaling pipeline."""
    return Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )


def fit_transform_biomarkers(frame: pd.DataFrame, features: Iterable[str]) -> PreprocessedMatrix:
    """Fit preprocessing on selected features and return transformed matrix."""
    feature_names = [feature for feature in features if feature in frame.columns]
    if not feature_names:
        raise ValueError("No requested biomarker features were found in the dataframe")
    values = frame[feature_names].apply(pd.to_numeric, errors="coerce")
    pipeline = build_preprocessing_pipeline()
    matrix = pipeline.fit_transform(values)
    return PreprocessedMatrix(
        matrix=np.asarray(matrix), feature_names=feature_names, pipeline=pipeline
    )


def transform_biomarkers(
    frame: pd.DataFrame, features: Iterable[str], pipeline: Pipeline
) -> np.ndarray:
    """Transform selected features using an already-fitted preprocessing pipeline."""
    feature_names = [feature for feature in features if feature in frame.columns]
    values = frame[feature_names].apply(pd.to_numeric, errors="coerce")
    return np.asarray(pipeline.transform(values))
