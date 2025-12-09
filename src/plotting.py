"""Reusable plotting helpers for notebooks."""
from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_context("talk")


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


def plot_pca_categorical(df, x="PC1", y="PC2", hue_col="sample_type", title=None):
    plt.figure(figsize=(10, 8))  # larger figure

    ax = sns.scatterplot(
        data=df,
        x=x,
        y=y,
        hue=hue_col,
        s=60,              # slightly larger points
        edgecolor="none",
        alpha=0.85,
    )

    ax.set_xlabel(x, fontsize=12)
    ax.set_ylabel(y, fontsize=12)

    if title is None:
        title = f"{x} vs {y} colored by {hue_col}"
    ax.set_title(title, fontsize=14)

    # Make legend text smaller
    legend = ax.legend(
        bbox_to_anchor=(1.05, 1),
        loc="upper left",
        borderaxespad=0.,
        title=hue_col,
        fontsize=8,       # smaller legend text
        title_fontsize=9  # smaller title text
    )

    plt.tight_layout()
    plt.show()

def plot_pca_continuous(df, x="PC1", y="PC2", color_col="concentration", title=None):
    plt.figure(figsize=(10, 8))  # larger figure

    sc = plt.scatter(
        df[x],
        df[y],
        c=df[color_col],
        s=60,          # larger points
        cmap="viridis",
        alpha=0.85
    )

    plt.xlabel(x, fontsize=12)
    plt.ylabel(y, fontsize=12)

    if title is None:
        title = f"{x} vs {y} colored by {color_col}"
    plt.title(title, fontsize=14)

    # Colorbar with smaller tick labels
    cbar = plt.colorbar(sc)
    cbar.set_label(color_col, fontsize=10)
    cbar.ax.tick_params(labelsize=8)  # smaller tick labels

    plt.tight_layout()
    plt.show()
