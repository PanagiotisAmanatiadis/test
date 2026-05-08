"""ENN — Edited Nearest Neighbour instance selection algorithm."""

import logging

import numpy as np
from sklearn.neighbors import NearestNeighbors

from instance_selection.data import Dataset
from instance_selection.selectors.base import BaseInstanceSelector

logger = logging.getLogger(__name__)


class ENNSelector(BaseInstanceSelector):
    """Edited Nearest Neighbour (Wilson, 1972).

    Removes instances that are misclassified by the majority vote of their
    *k* nearest neighbours within the same dataset.  Noisy and borderline
    instances — those surrounded mostly by points of a different class —
    are edited out, leaving a cleaner decision boundary.

    The removal condition (same as the original):
        remove instance *p* if fewer than ``k / 2`` of its *k* nearest
        neighbours share its class label  (i.e. same-class fraction < 0.5).

    Batch implementation: all k-NN queries are executed in a single call to
    ``sklearn.neighbors.NearestNeighbors`` (KD-tree / ball-tree), which is
    orders of magnitude faster than a per-point Python loop on large datasets.

    Args:
        k: Number of nearest neighbours used for the majority vote (default 3).
    """

    def __init__(self, k: int = 3) -> None:
        self._k = k

    def select(self, dataset: Dataset) -> Dataset:
        """Apply ENN to *dataset* and return the edited subset.

        Args:
            dataset: Normalised dataset.

        Returns:
            A :class:`Dataset` with noisy instances removed.
        """
        X, y = dataset.X, dataset.y
        logger.info(
            "ENN on '%s': %d instances (k=%d) …",
            dataset.name, len(X), self._k,
        )

        # k+1 neighbours because the first result is the point itself (dist=0)
        nbrs = NearestNeighbors(n_neighbors=self._k + 1, algorithm="auto", n_jobs=-1)
        nbrs.fit(X)
        _, indices = nbrs.kneighbors(X)          # shape: (n, k+1)

        neighbour_indices = indices[:, 1:]        # drop the self-neighbour column
        neighbour_classes = y[neighbour_indices]  # shape: (n, k)

        # Count how many neighbours share the same class as each point
        same_class_counts = (neighbour_classes == y[:, np.newaxis]).sum(axis=1)
        keep = (same_class_counts / self._k) >= 0.5

        selected_X = X[keep]
        selected_y = y[keep]

        logger.info(
            "ENN '%s': %d → %d instances (%.1f%% retained)",
            dataset.name, len(X), int(keep.sum()),
            100 * keep.mean(),
        )
        return Dataset(
            X=selected_X,
            y=selected_y,
            feature_names=dataset.feature_names,
            name=f"{dataset.name}_ENN",
        )
