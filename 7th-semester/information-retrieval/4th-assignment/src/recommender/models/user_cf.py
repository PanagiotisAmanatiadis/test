"""User-Based Collaborative Filtering with mean-centered cosine similarity."""

import logging

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from recommender.models.base import BaseRecommender

logger = logging.getLogger(__name__)


class UserBasedCF(BaseRecommender):
    """Memory-based user-user collaborative filtering.

    Each user's rating vector is mean-centered before computing cosine
    similarity (equivalent to the Pearson correlation on rated items).
    Predictions use the weighted average of the K most similar neighbours
    who have rated the target item, adjusted by the neighbour's mean rating.

    Prediction formula::

        pred(u, i) = μ_u + Σ_v [ sim(u,v) × (r_vi − μ_v) ] / Σ_v |sim(u,v)|

    Args:
        k: Number of nearest neighbours to use for each prediction.
    """

    def __init__(self, k: int = 30) -> None:
        self._k           = k
        self._matrix:     pd.DataFrame | None = None
        self._user_means: pd.Series    | None = None
        self._sim:        np.ndarray   | None = None
        self._user_index: dict[int, int]      = {}

    # ── public API ────────────────────────────────────────────────────────────

    def fit(self, train: pd.DataFrame) -> "UserBasedCF":
        logger.info("UserBasedCF.fit  k=%d  |  %d ratings", self._k, len(train))

        matrix          = self._build_matrix(train)
        self._user_means = self._user_means_from(matrix)
        self._matrix    = matrix

        # Mean-centre each user's row; fill missing with 0 (neutral)
        centered = matrix.sub(self._user_means, axis=0).fillna(0).to_numpy(dtype=np.float32)

        # Vectorised pairwise cosine similarity: shape (n_users, n_users)
        self._sim        = cosine_similarity(centered).astype(np.float32)
        self._user_index = {uid: i for i, uid in enumerate(matrix.index)}

        logger.info("Similarity matrix computed: %s", self._sim.shape)
        return self

    def predict_batch(self, pairs: pd.DataFrame) -> np.ndarray:
        assert self._matrix is not None, "Call fit() first."

        predictions = np.full(len(pairs), np.nan, dtype=np.float32)
        movie_cols  = {mid: i for i, mid in enumerate(self._matrix.columns)}

        for idx, (_, row) in enumerate(pairs.iterrows()):
            uid, mid = int(row["userId"]), int(row["movieId"])
            predictions[idx] = self._predict_one(uid, mid, movie_cols)

        return predictions

    # ── private ───────────────────────────────────────────────────────────────

    def _predict_one(
        self,
        user_id:    int,
        movie_id:   int,
        movie_cols: dict[int, int],
    ) -> float:
        if user_id not in self._user_index or movie_id not in movie_cols:
            return np.nan

        u_idx  = self._user_index[user_id]
        m_col  = movie_cols[movie_id]
        mu_u   = float(self._user_means.iloc[u_idx])

        sim_row = self._sim[u_idx]  # similarity of user_id to every other user

        # Ratings column for the target movie
        movie_ratings = self._matrix.iloc[:, m_col].to_numpy(dtype=np.float32)
        rated_mask    = ~np.isnan(movie_ratings)
        rated_mask[u_idx] = False  # exclude the target user

        if rated_mask.sum() == 0:
            return np.nan

        sims    = sim_row[rated_mask]
        ratings = movie_ratings[rated_mask]
        means   = self._user_means.to_numpy(dtype=np.float32)[rated_mask]

        # Keep only neighbours with positive similarity
        pos_mask = sims > 0
        if pos_mask.sum() == 0:
            return np.nan

        sims, ratings, means = sims[pos_mask], ratings[pos_mask], means[pos_mask]

        # Top-K neighbours
        if len(sims) > self._k:
            top_k = np.argpartition(sims, -self._k)[-self._k:]
            sims, ratings, means = sims[top_k], ratings[top_k], means[top_k]

        denom = np.sum(sims)
        if denom == 0:
            return np.nan

        predicted = mu_u + np.dot(sims, ratings - means) / denom
        return float(np.clip(predicted, 0.5, 5.0))

    @staticmethod
    def _user_means_from(matrix: pd.DataFrame) -> pd.Series:
        return matrix.mean(axis=1)
