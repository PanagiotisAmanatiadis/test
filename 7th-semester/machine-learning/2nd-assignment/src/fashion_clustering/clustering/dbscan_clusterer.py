"""DBSCAN clustering."""

from __future__ import annotations

import numpy as np
from loguru import logger
from sklearn.cluster import DBSCAN

from .base import AbstractClusterer


class DBSCANClusterer(AbstractClusterer):
    """DBSCAN density-based clustering algorithm."""

    def __init__(self, eps: float = 0.5, min_samples: int = 5) -> None:
        """Initialize DBSCANClusterer.

        Args:
            eps: Maximum distance between two samples in the same neighborhood.
            min_samples: Minimum number of samples in a neighborhood for a core point.
        """
        self._eps = eps
        self._min_samples = min_samples
        self._model = DBSCAN(eps=eps, min_samples=min_samples)
        self._n_clusters: int = 0
        logger.info(f"DBSCANClusterer initialized — eps={eps}, min_samples={min_samples}")

    def fit_predict(self, X: np.ndarray) -> np.ndarray:
        """Fit and predict cluster labels.

        Args:
            X: Data of shape (N, D).

        Returns:
            Labels of shape (N,). Noise points are labeled -1.
        """
        logger.info(f"Running DBSCAN on {X.shape}")
        labels = self._model.fit_predict(X)
        unique = set(labels)
        unique.discard(-1)
        self._n_clusters = len(unique)
        n_noise = int(np.sum(labels == -1))
        logger.info(f"DBSCAN found {self._n_clusters} clusters, {n_noise} noise points")
        if self._n_clusters == 0:
            logger.warning("DBSCAN found 0 clusters — all points classified as noise")
        return labels

    @property
    def name(self) -> str:
        """Human-readable name."""
        return "DBSCAN"

    @property
    def n_clusters(self) -> int:
        """Number of clusters found (excluding noise)."""
        return self._n_clusters
