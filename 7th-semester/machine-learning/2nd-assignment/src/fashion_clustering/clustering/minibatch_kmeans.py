"""MiniBatch K-Means clustering."""

from __future__ import annotations

import numpy as np
from loguru import logger
from sklearn.cluster import MiniBatchKMeans

from .base import AbstractClusterer


class MiniBatchKMeansClusterer(AbstractClusterer):
    """MiniBatch K-Means clustering algorithm."""

    def __init__(self, n_clusters: int = 10, batch_size: int = 1024, seed: int = 42) -> None:
        """Initialize MiniBatchKMeansClusterer.

        Args:
            n_clusters: Number of clusters.
            batch_size: Mini-batch size.
            seed: Random seed.
        """
        self._n_clusters = n_clusters
        self._model = MiniBatchKMeans(
            n_clusters=n_clusters, batch_size=batch_size, random_state=seed,
        )
        logger.info(f"MiniBatchKMeansClusterer initialized — k={n_clusters}")

    def fit_predict(self, X: np.ndarray) -> np.ndarray:
        """Fit and predict cluster labels.

        Args:
            X: Data of shape (N, D).

        Returns:
            Labels of shape (N,).
        """
        logger.info(f"Running MiniBatch K-Means on {X.shape}")
        labels = self._model.fit_predict(X)
        logger.info(f"MiniBatch K-Means found {self.n_clusters} clusters")
        return labels

    @property
    def name(self) -> str:
        """Human-readable name."""
        return "MiniBatchKMeans"

    @property
    def n_clusters(self) -> int:
        """Number of clusters."""
        return self._n_clusters
