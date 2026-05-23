"""Agglomerative (hierarchical) clustering."""

from __future__ import annotations

import numpy as np
from loguru import logger
from sklearn.cluster import AgglomerativeClustering

from .base import AbstractClusterer


class AgglomerativeClusterer(AbstractClusterer):
    """Agglomerative hierarchical clustering algorithm."""

    def __init__(self, n_clusters: int = 10, linkage: str = "ward") -> None:
        """Initialize AgglomerativeClusterer.

        Args:
            n_clusters: Number of clusters.
            linkage: Linkage criterion ('ward', 'complete', 'average', 'single').
        """
        self._n_clusters = n_clusters
        self._model = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage)
        logger.info(
            f"AgglomerativeClusterer initialized — n_clusters={n_clusters}, linkage={linkage}"
        )

    def fit_predict(self, X: np.ndarray) -> np.ndarray:
        """Fit and predict cluster labels.

        Args:
            X: Data of shape (N, D).

        Returns:
            Labels of shape (N,).
        """
        logger.info(f"Running Agglomerative Clustering on {X.shape}")
        labels = self._model.fit_predict(X)
        logger.info(f"Agglomerative found {self.n_clusters} clusters")
        return labels

    @property
    def name(self) -> str:
        """Human-readable name."""
        return "Agglomerative"

    @property
    def n_clusters(self) -> int:
        """Number of clusters."""
        return self._n_clusters
