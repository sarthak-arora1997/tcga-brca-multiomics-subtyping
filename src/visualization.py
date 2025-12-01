"""Visualization helpers for embeddings and survival analysis."""
from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


sns.set_context("talk")


def plot_embedding(embedding: pd.DataFrame, hue: pd.Series | None = None, *, title: str = "Embedding") -> plt.Axes:
    """Scatter plot of a 2D embedding (PCA/UMAP/t-SNE)."""

    if embedding.shape[1] < 2:
        raise ValueError("Embedding must have at least two columns for plotting")

    ax = sns.scatterplot(
        x=embedding.iloc[:, 0],
        y=embedding.iloc[:, 1],
        hue=hue,
        palette="tab10" if hue is not None else None,
        s=60,
        edgecolor="white",
    )
    ax.set_xlabel(embedding.columns[0])
    ax.set_ylabel(embedding.columns[1])
    ax.set_title(title)
    return ax
