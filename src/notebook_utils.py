"""Helper utilities shared across data organization notebooks."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


def collect_expression_files(root: Path, pattern: str = "*.tsv") -> pd.DataFrame:
    """Return a manifest of expression files located under ``root``."""

    root = Path(root)
    if not root.exists():
        raise FileNotFoundError(f"Expression directory not found: {root}")

    records: list[dict[str, object]] = []
    for bundle in sorted(p for p in root.iterdir() if p.is_dir()):
        for path in sorted(bundle.glob(pattern)):
            if path.suffix.lower() == ".txt":
                continue
            records.append(
                {
                    "file_name": path.name,
                    "bundle_id": bundle.name,
                    "path": path,
                    "relative_path": path.relative_to(root).as_posix(),
                }
            )

    if not records:
        raise FileNotFoundError(f"No files matching {pattern} discovered under {root}")
    return pd.DataFrame.from_records(records)


def flatten_metadata_column(metadata: pd.DataFrame, column: str, value_cols: Iterable[str]) -> pd.DataFrame:
    """Explode a nested metadata column and aggregate requested fields per ``file_name``."""

    if column not in metadata:
        return pd.DataFrame(columns=["file_name", *value_cols])

    exploded = metadata[["file_name", column]].explode(column).dropna(subset=[column])
    if exploded.empty:
        return pd.DataFrame(columns=["file_name", *value_cols])

    nested = exploded[column].apply(pd.Series)
    if nested is None or nested.empty:
        return pd.DataFrame(columns=["file_name", *value_cols])

    available_cols = [col for col in value_cols if col in nested.columns]
    if not available_cols:
        return pd.DataFrame(columns=["file_name", *value_cols])

    expanded = pd.concat(
        [exploded[["file_name"]].reset_index(drop=True), nested[available_cols].reset_index(drop=True)],
        axis=1,
    )
    grouped = (
        expanded.groupby("file_name")[available_cols]
        .agg(lambda s: ";".join(sorted({str(v) for v in s.dropna()})))
        .reset_index()
    )

    for col in value_cols:
        if col not in grouped.columns:
            grouped[col] = ""

    return grouped[["file_name", *value_cols]]


def summarize_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Return percentage of missing values per column sorted descending."""

    if df.empty:
        return pd.DataFrame(columns=["column_name", "missing_percentage"])

    missing_summary = df.isna().mean().mul(100).reset_index()
    missing_summary.columns = ["column_name", "missing_percentage"]
    return missing_summary.sort_values(by="missing_percentage", ascending=False, kind="mergesort").reset_index(drop=True)
