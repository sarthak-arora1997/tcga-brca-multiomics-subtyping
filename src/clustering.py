"""Unsupervised clustering helpers for expression embeddings."""
from __future__ import annotations

import pandas as pd
from sklearn.cluster import AgglomerativeClustering, KMeans


def kmeans_clustering(embedding: pd.DataFrame, n_clusters: int = 4, *, random_state: int = 42) -> pd.Series:
    """Cluster rows of ``embedding`` with k-means."""

    model = KMeans(n_clusters=n_clusters, n_init="auto", random_state=random_state)
    labels = model.fit_predict(embedding)
    return pd.Series(labels, index=embedding.index, name="cluster")


def hierarchical_clustering(embedding: pd.DataFrame, n_clusters: int = 4, linkage: str = "ward") -> pd.Series:
    """Agglomerative clustering wrapper."""

    model = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage)
    labels = model.fit_predict(embedding)
    return pd.Series(labels, index=embedding.index, name="cluster")
