"""Dimensionality reduction workflows (PCA, UMAP)."""
from __future__ import annotations

import pandas as pd
from sklearn.decomposition import PCA

try:
    import umap
except ImportError:  # pragma: no cover - placeholder project scaffold
    umap = None


def run_pca(
    matrix: pd.DataFrame, n_components: int = 50, *, return_model: bool = False
) -> pd.DataFrame | tuple[pd.DataFrame, PCA]:
    """Project matrix with PCA and return component scores (and optionally the PCA model)."""

    pca = PCA(n_components=n_components, random_state=42)
    components = pca.fit_transform(matrix.T)
    cols = [f"PC{i+1}" for i in range(components.shape[1])]
    scores = pd.DataFrame(components, index=matrix.columns, columns=cols)
    if return_model:
        return scores, pca
    return scores


def run_umap(embedding_input: pd.DataFrame, n_neighbors: int = 15, min_dist: float = 0.3) -> pd.DataFrame:
    """Run UMAP on the (typically PCA-reduced) data matrix."""

    if umap is None:
        raise ImportError("umap-learn must be installed to use UMAP projections")
    reducer = umap.UMAP(random_state=42, n_neighbors=n_neighbors, min_dist=min_dist)
    embedding = reducer.fit_transform(embedding_input)
    cols = [f"UMAP{i+1}" for i in range(embedding.shape[1])]
    return pd.DataFrame(embedding, index=embedding_input.index, columns=cols)
