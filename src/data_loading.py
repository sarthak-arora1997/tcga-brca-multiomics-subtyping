"""Data loading utilities for TCGA-BRCA files."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd

from .config import ProjectConfig

_DEFAULT_CONFIG = ProjectConfig()


def _resolve_path(path: Optional[Path], fallback: Path) -> Path:
    target = Path(path) if path else fallback
    if not target.exists():
        raise FileNotFoundError(f"Expected data file missing: {target}")
    return target


def load_expression_matrix(path: Optional[Path] = None, *, config: ProjectConfig = _DEFAULT_CONFIG) -> pd.DataFrame:
    """Load a processed expression matrix."""

    default = config.processed_data_dir / "expression_matrix.csv"
    file_path = _resolve_path(path, default)
    return pd.read_csv(file_path, index_col=0)


def load_clinical_table(path: Optional[Path] = None, *, config: ProjectConfig = _DEFAULT_CONFIG) -> pd.DataFrame:
    """Load clinical annotations for BRCA cases."""

    default = config.processed_data_dir / "clinical_data.csv"
    file_path = _resolve_path(path, default)
    return pd.read_csv(file_path)
