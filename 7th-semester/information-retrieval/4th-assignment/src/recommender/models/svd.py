"""SVD-based matrix factorisation recommender (baseline + latent factors)."""

import logging

import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD

from recommender.models.base import BaseRecommender

logger = logging.getLogger(__name__)


class SVDRecommender(BaseRecommender):
    """Matrix-factorisation recommender using truncated SVD with bias terms.

    The rating matrix is decomposed as::

        R ≈ global_mean + B_u + B_i + U × Σ × V^T

    where B_u and B_i are per-user and per-item bias vectors learned from the
    training data.  The residual matrix (ratings minus biases) is factorised by
    :class:`~sklearn.decomposition.TruncatedSVD`.

    Args:
        n_factors: Number of latent factors (rank of the approximation).
    """

    def __init__(self, n_factors: int = 50) -> None:
        self._n_factors   = n_factors
        self._global_mean = 0.0
        self._user_bias:  pd.Series    | None = None
        self._item_bias:  pd.Series    | None = None
        self._R_hat:      pd.DataFrame | None = None  # full reconstructed matrix

    # ── public API ────────────────────────────────────────────────────────────

    def fit(self, train: pd.DataFrame) -> "SVDRecommender":
        logger.info("SVDRecommender.fit  n_factors=%d  |  %d ratings", self._n_factors, len(train))

        self._global_mean = float(train["rating"].mean())

        # Compute biases: user_bias_u = mean(R_ui) − global_mean
        self._user_bias = train.groupby("userId")["rating"].mean() - self._global_mean
        self._item_bias = train.groupby("movieId")["rating"].mean() - self._global_mean

        # Build residual matrix (subtract biases)
        def residual(row: pd.Series) -> float:
            return (
                row["rating"]
                - self._global_mean
                - self._user_bias.get(row["userId"], 0.0)
                - self._item_bias.get(row["movieId"], 0.0)
            )

        train = train.copy()
        train["residual"] = train.apply(residual, axis=1)

        # Pivot to (users × movies) — missing entries filled with 0
        R = train.pivot(index="userId", columns="movieId", values="residual").fillna(0.0)
        R_np = R.to_numpy(dtype=np.float32)

        # Truncated SVD: R ≈ U × S × V^T
        svd = TruncatedSVD(n_components=self._n_factors, random_state=42)
        U   = svd.fit_transform(R_np)           # shape: (n_users, n_factors)
        V   = svd.components_                    # shape: (n_factors, n_movies)

        R_approx = U @ V                         # reconstructed residuals

        # Reconstruct full rating matrix: add back biases
        R_hat = pd.DataFrame(R_approx, index=R.index, columns=R.columns)
        R_hat = R_hat.add(self._user_bias, axis=0).fillna(R_hat)
        R_hat = R_hat.add(self._item_bias, axis=1).fillna(R_hat)
        R_hat += self._global_mean
        self._R_hat = np.clip(R_hat, 0.5, 5.0)

        explained = svd.explained_variance_ratio_.sum()
        logger.info(
            "SVD complete: %d factors explain %.1f%% of variance",
            self._n_factors, 100 * explained,
        )
        return self

    def predict_batch(self, pairs: pd.DataFrame) -> np.ndarray:
        assert self._R_hat is not None, "Call fit() first."

        predictions = np.full(len(pairs), np.nan, dtype=np.float32)

        users  = set(self._R_hat.index)
        movies = set(self._R_hat.columns)

        for idx, (_, row) in enumerate(pairs.iterrows()):
            uid, mid = int(row["userId"]), int(row["movieId"])
            if uid in users and mid in movies:
                predictions[idx] = float(self._R_hat.at[uid, mid])

        return predictions
