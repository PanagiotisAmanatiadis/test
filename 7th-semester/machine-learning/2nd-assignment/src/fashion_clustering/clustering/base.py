"""Abstract base class for clustering strategies."""

from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np


class AbstractClusterer(ABC):
    """Strategy interface for all clustering algorithms."""

    @abstractmethod
    def fit_predict(self, X: np.ndarray) -> np.ndarray:
        """Fit on X and return integer cluster labels.

        Args:
            X: Data to cluster, shape (N, D).

        Returns:
            Cluster labels of shape (N,).
        """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable algorithm name used in DataFrame and plots."""

    @property
    def n_clusters(self) -> int:
        """Number of clusters found (available after fit_predict).

        Returns:
            Number of unique clusters.

        Raises:
            NotImplementedError: If not implemented by subclass.
        """
        raise NotImplementedError
