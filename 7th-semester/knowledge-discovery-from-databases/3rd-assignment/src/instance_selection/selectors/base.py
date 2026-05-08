"""Abstract base class and shared vectorised k-NN helper."""

from abc import ABC, abstractmethod

import numpy as np

from instance_selection.data import Dataset


class BaseInstanceSelector(ABC):
    """Common interface for instance selection algorithms.

    Subclasses implement :meth:`select`, which receives a :class:`Dataset`
    and returns a reduced :class:`Dataset` containing only the selected
    instances.
    """

    @abstractmethod
    def select(self, dataset: Dataset) -> Dataset:
        """Return a subset of *dataset* according to the selection rule.

        Args:
            dataset: Normalised dataset produced by :class:`~instance_selection.data.DataLoader`.

        Returns:
            A new :class:`Dataset` containing only the selected instances.
        """

    # ── shared helpers ────────────────────────────────────────────────────────

    @staticmethod
    def _k_nearest_classes(
        pool_X: np.ndarray,
        pool_y: np.ndarray,
        query:  np.ndarray,
        k:      int,
    ) -> np.ndarray:
        """Return the class labels of the *k* nearest neighbours to *query*.

        Points whose distance to *query* is exactly 0 (i.e. the query itself)
        are excluded by setting their distance to infinity before selection.

        Uses vectorised L2 distances via ``np.linalg.norm`` — no Python loop
        over the pool, so this scales well to tens of thousands of points.

        Args:
            pool_X: Feature matrix of the candidate pool, shape (n, d).
            pool_y: Class label array, shape (n,).
            query:  Feature vector to classify, shape (d,).
            k:      Number of neighbours to return.

        Returns:
            Array of *k* class labels (may be fewer if the pool is smaller).
        """
        distances        = np.linalg.norm(pool_X - query, axis=1)
        distances[distances == 0.0] = np.inf   # exclude the query point itself

        effective_k = min(k, int(np.isfinite(distances).sum()))
        if effective_k == 0:
            return np.array([], dtype=pool_y.dtype)

        idx = np.argpartition(distances, effective_k - 1)[:effective_k]
        return pool_y[idx]
