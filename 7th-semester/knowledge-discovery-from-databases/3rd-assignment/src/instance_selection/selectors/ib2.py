"""IB2 — Instance-Based Learning 2 instance selection algorithm."""

import logging

import numpy as np

from instance_selection.data import Dataset
from instance_selection.selectors.base import BaseInstanceSelector

logger = logging.getLogger(__name__)


class IB2Selector(BaseInstanceSelector):
    """IB2 instance selection (Aha, Kibler & Albert, 1991).

    Builds a minimal *concept set* (CS) from the training data using a
    single pass:

    1. Initialise CS with the first instance.
    2. For each remaining instance *p*:
       - Classify *p* using 1-NN from CS.
       - If *p* is misclassified, add it to CS.

    The resulting CS is the smallest subset that correctly classifies all
    training instances it was built from (under the 1-NN rule).  Points that
    are correctly classified by the current CS are redundant and discarded.
    """

    def select(self, dataset: Dataset) -> Dataset:
        """Apply IB2 to *dataset* and return the selected concept set.

        Args:
            dataset: Normalised dataset.

        Returns:
            A :class:`Dataset` containing only the selected instances.
        """
        X, y = dataset.X, dataset.y
        logger.info("IB2 on '%s': %d instances …", dataset.name, len(X))

        cs_indices: list[int] = [0]   # concept set starts with the first instance

        for i in range(1, len(X)):
            cs_X = X[cs_indices]
            cs_y = y[cs_indices]

            nn_classes = self._k_nearest_classes(cs_X, cs_y, X[i], k=1)

            if len(nn_classes) == 0 or nn_classes[0] != y[i]:
                cs_indices.append(i)

        selected_X = X[cs_indices]
        selected_y = y[cs_indices]

        logger.info(
            "IB2 '%s': %d → %d instances (%.1f%% retained)",
            dataset.name, len(X), len(cs_indices),
            100 * len(cs_indices) / len(X),
        )
        return Dataset(
            X=selected_X,
            y=selected_y,
            feature_names=dataset.feature_names,
            name=f"{dataset.name}_IB2",
        )
