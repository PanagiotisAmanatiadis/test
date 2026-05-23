"""Gaussian Mixture Model clustering."""

from __future__ import annotations

import numpy as np
from loguru import logger
from sklearn.mixture import GaussianMixture

from .base import AbstractClusterer


class GMMClusterer(AbstractClusterer):
    """Gaussian Mixture Model clustering algorithm."""

    def __init__(
        self,
        n_components: int = 10,
        covariance_type: str = "full",
        seed: int = 42,
    ) -> None:
        """Initialize GMMClusterer.

        Args:
            n_components: Number of mixture components.
            covariance_type: Type of covariance parameters.
            seed: Random seed.
        """
        self._n_components = n_components
        self._model = GaussianMixture(
            n_components=n_components,
            covariance_type=covariance_type,
            random_state=seed,
        )
        logger.info(
            f"GMMClusterer initialized — n_components={n_components}, "
            f"covariance_type={covariance_type}"
        )

    def fit_predict(self, X: np.ndarray) -> np.ndarray:
        """Fit and predict cluster labels.

        Args:
            X: Data of shape (N, D).

        Returns:
            Labels of shape (N,).
        """
        logger.info(f"Running GMM on {X.shape}")
        labels = self._model.fit_predict(X)
        logger.info(f"GMM found {self.n_clusters} components")
        return labels

    @property
    def name(self) -> str:
        """Human-readable name."""
        return "GMM"

    @property
    def n_clusters(self) -> int:
        """Number of components."""
        return self._n_components
