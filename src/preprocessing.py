"""Preprocessing helpers for RNA-seq expression matrices."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


def filter_low_expression(matrix: pd.DataFrame, min_mean: float = 1.0) -> pd.DataFrame:
    """Drop genes whose mean expression is below ``min_mean``."""

    mask = matrix.mean(axis=1) >= min_mean
    return matrix.loc[mask]


def log_transform(matrix: pd.DataFrame, pseudo_count: float = 1.0) -> pd.DataFrame:
    """Apply log2 transformation with a pseudo count to stabilize variance."""

    return np.log2(matrix + pseudo_count)


def scale_features(matrix: pd.DataFrame) -> pd.DataFrame:
    """Z-score scale features across samples."""

    scaler = StandardScaler()
    scaled = scaler.fit_transform(matrix.T).T  # scale per gene
    return pd.DataFrame(scaled, index=matrix.index, columns=matrix.columns)
