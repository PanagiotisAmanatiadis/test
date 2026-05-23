"""HDBSCAN clustering."""

from __future__ import annotations

import numpy as np
from loguru import logger
from hdbscan import HDBSCAN

from .base import AbstractClusterer


class HDBSCANClusterer(AbstractClusterer):
    """HDBSCAN hierarchical density-based clustering algorithm."""

    def __init__(self, min_cluster_size: int = 50) -> None:
        """Initialize HDBSCANClusterer.

        Args:
            min_cluster_size: Minimum size of clusters.
        """
        self._min_cluster_size = min_cluster_size
        self._model = HDBSCAN(min_cluster_size=min_cluster_size)
        self._n_clusters: int = 0
        logger.info(f"HDBSCANClusterer initialized — min_cluster_size={min_cluster_size}")

    def fit_predict(self, X: np.ndarray) -> np.ndarray:
        """Fit and predict cluster labels.

        Args:
            X: Data of shape (N, D).

        Returns:
            Labels of shape (N,). Noise points are labeled -1.
        """
        logger.info(f"Running HDBSCAN on {X.shape}")
        labels = self._model.fit_predict(X)
        unique = set(labels)
        unique.discard(-1)
        self._n_clusters = len(unique)
        n_noise = int(np.sum(labels == -1))
        logger.info(f"HDBSCAN found {self._n_clusters} clusters, {n_noise} noise points")
        return labels

    @property
    def name(self) -> str:
        """Human-readable name."""
        return "HDBSCAN"

    @property
    def n_clusters(self) -> int:
        """Number of clusters found (excluding noise)."""
        return self._n_clusters
