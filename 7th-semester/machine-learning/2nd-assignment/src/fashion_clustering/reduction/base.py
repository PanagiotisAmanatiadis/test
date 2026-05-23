"""Abstract base class for dimensionality reduction strategies."""

from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np


class AbstractReducer(ABC):
    """Strategy interface for all dimensionality reduction techniques."""

    @abstractmethod
    def fit(self, X_train: np.ndarray, X_val: np.ndarray | None = None) -> AbstractReducer:
        """Fit the reducer on training (and optionally validation) data.

        Args:
            X_train: Training data.
            X_val: Optional validation data (used by NN-based reducers).

        Returns:
            Self for method chaining.
        """

    @abstractmethod
    def transform(self, X: np.ndarray) -> np.ndarray:
        """Encode X into the latent space.

        Args:
            X: Input data to transform.

        Returns:
            Transformed data in lower-dimensional space.
        """

    def fit_transform(self, X_train: np.ndarray, X_val: np.ndarray | None = None) -> np.ndarray:
        """Fit on X_train and return transformed X_train.

        Args:
            X_train: Training data.
            X_val: Optional validation data.

        Returns:
            Transformed training data.
        """
        return self.fit(X_train, X_val).transform(X_train)

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable technique name used in DataFrame and plots."""

    def reconstruct(self, X: np.ndarray) -> np.ndarray | None:
        """Reconstruct images from latent codes.

        Args:
            X: Original input data (not latent codes).

        Returns:
            Reconstructed data, or None if unsupported.
        """
        return None
