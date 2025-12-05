"""Reusable plotting helpers for notebooks."""
from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def scatter_embedding(
    data: pd.DataFrame,
    *,
    x: str,
    y: str,
    hue: pd.Series | None = None,
    title: str = "",
    xlabel: str | None = None,
    ylabel: str | None = None,
    scatter_kwargs: dict[str, Any] | None = None,
) -> plt.Axes:
    """Create a scatter plot for 2D embeddings (e.g., t-SNE or UMAP)."""

    scatter_kwargs = scatter_kwargs or {}
    defaults = {"edgecolor": "white", "s": 60}
    defaults.update(scatter_kwargs)
    ax = sns.scatterplot(
        data=data,
        x=x,
        y=y,
        hue=hue,
        palette="tab10" if hue is not None else None,
        **defaults,
    )
    ax.set_title(title)
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    return ax
