"""Item-Based Collaborative Filtering with adjusted cosine similarity."""

import logging

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from recommender.models.base import BaseRecommender

logger = logging.getLogger(__name__)


class ItemBasedCF(BaseRecommender):
    """Memory-based item-item collaborative filtering.

    Adjusted cosine similarity is computed between items by first subtracting
    each *user's* mean rating from every item that user has rated, removing
    the per-user rating bias before measuring item similarity.

    Prediction formula::

        pred(u, i) = Σ_j [ sim(i,j) × r_uj ] / Σ_j |sim(i,j)|

    where j ranges over the K most similar items that user u has already rated.

    Args:
        k: Number of most-similar rated items to use per prediction.
    """

    def __init__(self, k: int = 30) -> None:
        self._k           = k
        self._matrix:     pd.DataFrame | None = None
        self._sim:        np.ndarray   | None = None
        self._item_index: dict[int, int]      = {}

    # ── public API ────────────────────────────────────────────────────────────

    def fit(self, train: pd.DataFrame) -> "ItemBasedCF":
        logger.info("ItemBasedCF.fit  k=%d  |  %d ratings", self._k, len(train))

        matrix = self._build_matrix(train)
        self._matrix = matrix

        # Adjusted cosine: subtract each user's mean from all their ratings
        user_means = matrix.mean(axis=1)
        centered   = matrix.sub(user_means, axis=0).fillna(0)

        # Item vectors are the *columns* of the centered matrix (shape: n_items × n_users)
        item_vectors = centered.to_numpy(dtype=np.float32).T

        # Vectorised cosine similarity between items: shape (n_items, n_items)
        self._sim = cosine_similarity(item_vectors).astype(np.float32)
        np.fill_diagonal(self._sim, 0)  # exclude self-similarity

        self._item_index = {mid: i for i, mid in enumerate(matrix.columns)}

        logger.info("Item similarity matrix computed: %s", self._sim.shape)
        return self

    def predict_batch(self, pairs: pd.DataFrame) -> np.ndarray:
        assert self._matrix is not None, "Call fit() first."

        predictions = np.full(len(pairs), np.nan, dtype=np.float32)

        for idx, (_, row) in enumerate(pairs.iterrows()):
            uid, mid = int(row["userId"]), int(row["movieId"])
            predictions[idx] = self._predict_one(uid, mid)

        return predictions

    # ── private ───────────────────────────────────────────────────────────────

    def _predict_one(self, user_id: int, movie_id: int) -> float:
        if movie_id not in self._item_index:
            return np.nan
        if user_id not in self._matrix.index:
            return np.nan

        i_idx = self._item_index[movie_id]
        sim_row = self._sim[i_idx]  # similarity of target item to all other items

        # Ratings by this user for all items
        user_row = self._matrix.loc[user_id].to_numpy(dtype=np.float32)
        rated_mask = ~np.isnan(user_row)

        if rated_mask.sum() == 0:
            return np.nan

        sims    = sim_row[rated_mask]
        ratings = user_row[rated_mask]

        pos_mask = sims > 0
        if pos_mask.sum() == 0:
            return np.nan

        sims, ratings = sims[pos_mask], ratings[pos_mask]

        # Top-K most similar rated items
        if len(sims) > self._k:
            top_k = np.argpartition(sims, -self._k)[-self._k:]
            sims, ratings = sims[top_k], ratings[top_k]

        denom = np.sum(sims)
        if denom == 0:
            return np.nan

        predicted = np.dot(sims, ratings) / denom
        return float(np.clip(predicted, 0.5, 5.0))
