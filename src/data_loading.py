"""Data loading utilities for TCGA-BRCA files."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd

from .config import ProjectConfig

_DEFAULT_CONFIG = ProjectConfig()
_TSV_KWARGS: dict[str, object] = {"sep": "\t", "index_col": 0}


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


def load_expression_tpm(path: Optional[Path] = None, *, config: ProjectConfig = _DEFAULT_CONFIG) -> pd.DataFrame:
    """Load the processed TPM expression matrix persisted by notebook 01."""

    default = config.processed_data_dir / "tcga_brca_expression_tpm.tsv.gz"
    file_path = _resolve_path(path, default)
    return pd.read_csv(file_path, compression="gzip", **_TSV_KWARGS)


def load_expression_manifest(path: Optional[Path] = None, *, config: ProjectConfig = _DEFAULT_CONFIG) -> pd.DataFrame:
    """Load the enriched expression-file manifest (biospecimen metadata)."""

    default = config.processed_data_dir / "expression_file_index.tsv"
    file_path = _resolve_path(path, default)
    return pd.read_csv(file_path, sep="\t")


def load_pca_scores(path: Optional[Path] = None, *, config: ProjectConfig = _DEFAULT_CONFIG) -> pd.DataFrame:
    """Load the PCA scores generated in notebook 02."""

    default = config.processed_data_dir / "tcga_brca_pca_scores.tsv.gz"
    file_path = _resolve_path(path, default)
    return pd.read_csv(file_path, compression="gzip", **_TSV_KWARGS)


def load_embedding(name: str, path: Optional[Path] = None, *, config: ProjectConfig = _DEFAULT_CONFIG) -> pd.DataFrame:
    """Load a saved 2D embedding (t-SNE/UMAP) by name."""

    default = config.processed_data_dir / f"tcga_brca_{name.lower()}.tsv.gz"
    file_path = _resolve_path(path, default)
    return pd.read_csv(file_path, compression="gzip", **_TSV_KWARGS)
