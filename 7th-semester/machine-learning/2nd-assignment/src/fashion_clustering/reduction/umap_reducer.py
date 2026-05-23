"""UMAP dimensionality reduction."""

from __future__ import annotations

import numpy as np
from loguru import logger
from umap import UMAP

from .base import AbstractReducer


class UMAPReducer(AbstractReducer):
    """Uniform Manifold Approximation and Projection reducer."""

    def __init__(
        self,
        n_components: int = 32,
        n_neighbors: int = 15,
        min_dist: float = 0.1,
        seed: int = 42,
    ) -> None:
        """Initialize UMAPReducer.

        Args:
            n_components: Target dimensionality.
            n_neighbors: Number of neighbors for UMAP.
            min_dist: Minimum distance parameter.
            seed: Random seed.
        """
        self._umap = UMAP(
            n_components=n_components,
            n_neighbors=n_neighbors,
            min_dist=min_dist,
            random_state=seed,
        )
        logger.info(
            f"UMAPReducer initialized — n_components={n_components}, "
            f"n_neighbors={n_neighbors}, min_dist={min_dist}"
        )

    def fit(self, X_train: np.ndarray, X_val: np.ndarray | None = None) -> UMAPReducer:
        """Fit UMAP on training data.

        Args:
            X_train: Training data of shape (N, D).
            X_val: Ignored for UMAP.

        Returns:
            Self.
        """
        logger.info(f"Fitting UMAP on data with shape {X_train.shape}")
        self._umap.fit(X_train)
        logger.info("UMAP fit complete")
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Transform data using fitted UMAP.

        Args:
            X: Data of shape (N, D).

        Returns:
            Transformed data of shape (N, n_components).
        """
        Z = self._umap.transform(X)
        logger.debug(f"UMAP transform: {X.shape} -> {Z.shape}")
        return Z

    @property
    def name(self) -> str:
        """Human-readable name."""
        return "UMAP"
