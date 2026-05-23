"""PCA dimensionality reduction."""

from __future__ import annotations

import numpy as np
from loguru import logger
from sklearn.decomposition import PCA

from .base import AbstractReducer


class PCAReducer(AbstractReducer):
    """Principal Component Analysis reducer.

    Attributes:
        pca: Fitted sklearn PCA instance (available after fit).
    """

    def __init__(self, n_components: int = 50) -> None:
        """Initialize PCAReducer.

        Args:
            n_components: Number of principal components to keep.
        """
        self._n_components = n_components
        self.pca: PCA | None = None
        logger.info(f"PCAReducer initialized with n_components={n_components}")

    def fit(self, X_train: np.ndarray, X_val: np.ndarray | None = None) -> PCAReducer:
        """Fit PCA on training data.

        Args:
            X_train: Training data of shape (N, D).
            X_val: Ignored for PCA.

        Returns:
            Self.
        """
        logger.info(f"Fitting PCA on data with shape {X_train.shape}")
        self.pca = PCA(n_components=self._n_components)
        self.pca.fit(X_train)
        explained = self.pca.explained_variance_ratio_.sum()
        logger.info(f"PCA fit complete — explained variance: {explained:.4f}")
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Transform data using fitted PCA.

        Args:
            X: Data of shape (N, D).

        Returns:
            Transformed data of shape (N, n_components).
        """
        Z = self.pca.transform(X)
        logger.debug(f"PCA transform: {X.shape} -> {Z.shape}")
        return Z

    def reconstruct(self, X: np.ndarray) -> np.ndarray | None:
        """Reconstruct data via PCA inverse transform.

        Args:
            X: Original data of shape (N, D).

        Returns:
            Reconstructed data of shape (N, D).
        """
        Z = self.pca.transform(X)
        return self.pca.inverse_transform(Z)

    @property
    def name(self) -> str:
        """Human-readable name."""
        return "PCA"
