"""Data loading, filtering, and train/test splitting for the rating dataset."""

import logging
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SplitData:
    """Holds train and test DataFrames after the dataset is partitioned."""

    train: pd.DataFrame
    test: pd.DataFrame


class DataLoader:
    """Loads a MovieLens-style CSV and prepares filtered train/test splits.

    Args:
        min_user_ratings: Drop users with fewer ratings than this threshold.
        min_movie_ratings: Drop movies with fewer ratings than this threshold.
    """

    def __init__(self, min_user_ratings: int = 50, min_movie_ratings: int = 50) -> None:
        self._min_user  = min_user_ratings
        self._min_movie = min_movie_ratings

    def load(self, path: Path) -> pd.DataFrame:
        """Read the CSV, drop timestamp, coerce types, and apply activity filters.

        Args:
            path: Path to the ratings CSV (userId, movieId, rating[, timestamp]).

        Returns:
            Cleaned DataFrame with columns [userId, movieId, rating].
        """
        logger.info("Loading ratings from %s", path)
        ratings = pd.read_csv(path, usecols=["userId", "movieId", "rating"])
        ratings = ratings.dropna()
        ratings["rating"] = ratings["rating"].astype(np.float32)
        ratings["userId"]  = ratings["userId"].astype(np.int32)
        ratings["movieId"] = ratings["movieId"].astype(np.int32)

        before = len(ratings)
        ratings = self._filter(ratings)
        logger.info(
            "After filtering: %d → %d ratings  (%d users, %d movies)",
            before, len(ratings),
            ratings["userId"].nunique(),
            ratings["movieId"].nunique(),
        )
        return ratings

    def split(self, ratings: pd.DataFrame, test_frac: float = 0.2) -> SplitData:
        """Stratified random split: sample *test_frac* of each user's ratings.

        Stratifying by user ensures every user appears in both splits, which
        avoids the cold-start problem for evaluation.

        Args:
            ratings:   Cleaned DataFrame from :meth:`load`.
            test_frac: Fraction of rows to hold out for testing (0 < frac < 1).

        Returns:
            :class:`SplitData` with train and test DataFrames.
        """
        if not 0 < test_frac < 1:
            raise ValueError(f"test_frac must be in (0, 1), got {test_frac}")

        rng = np.random.default_rng(seed=42)

        test_idx = (
            ratings.groupby("userId", group_keys=False)
            .apply(
                lambda g: g.sample(frac=test_frac, random_state=int(rng.integers(1 << 31))),
                include_groups=False,
            )
            .index
        )
        test  = ratings.loc[test_idx].reset_index(drop=True)
        train = ratings.drop(index=test_idx).reset_index(drop=True)

        logger.info(
            "Train: %d ratings | Test: %d ratings (%.0f%% held out)",
            len(train), len(test), 100 * test_frac,
        )
        return SplitData(train=train, test=test)

    # ── private ───────────────────────────────────────────────────────────────

    def _filter(self, ratings: pd.DataFrame) -> pd.DataFrame:
        for _ in range(5):  # iterate until stable (users/movies may drop each other)
            user_counts  = ratings.groupby("userId")["movieId"].count()
            movie_counts = ratings.groupby("movieId")["userId"].count()
            active_users  = user_counts[user_counts  >= self._min_user].index
            active_movies = movie_counts[movie_counts >= self._min_movie].index
            filtered = ratings[
                ratings["userId"].isin(active_users) &
                ratings["movieId"].isin(active_movies)
            ]
            if len(filtered) == len(ratings):
                break
            ratings = filtered
        return ratings.reset_index(drop=True)
