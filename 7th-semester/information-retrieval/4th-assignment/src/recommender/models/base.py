"""Abstract base class shared by all recommendation models."""

from abc import ABC, abstractmethod

import numpy as np
import pandas as pd


class BaseRecommender(ABC):
    """Common interface for all recommender models.

    Subclasses implement :meth:`fit` to learn from the training set and
    :meth:`predict_batch` to generate rating predictions for a test DataFrame.
    """

    @abstractmethod
    def fit(self, train: pd.DataFrame) -> "BaseRecommender":
        """Train on *train* ratings.

        Args:
            train: DataFrame with columns [userId, movieId, rating].

        Returns:
            self (for chaining).
        """

    @abstractmethod
    def predict_batch(self, pairs: pd.DataFrame) -> np.ndarray:
        """Predict ratings for each (userId, movieId) pair.

        Args:
            pairs: DataFrame with at least [userId, movieId] columns.

        Returns:
            1-D float array of the same length as *pairs*.  Use ``np.nan``
            where a prediction cannot be made (cold-start, no neighbours).
        """

    # ── shared helpers ────────────────────────────────────────────────────────

    @staticmethod
    def _build_matrix(ratings: pd.DataFrame) -> pd.DataFrame:
        """Pivot ratings into a (users × movies) dense matrix."""
        return ratings.pivot(index="userId", columns="movieId", values="rating")

    @staticmethod
    def _user_means(matrix: pd.DataFrame) -> pd.Series:
        return matrix.mean(axis=1)

    @staticmethod
    def _item_means(matrix: pd.DataFrame) -> pd.Series:
        return matrix.mean(axis=0)
