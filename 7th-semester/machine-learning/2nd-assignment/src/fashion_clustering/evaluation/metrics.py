"""Clustering evaluation metrics."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from loguru import logger
from sklearn.metrics import (
    adjusted_rand_score,
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_score,
)


@dataclass
class MetricsResult:
    """Container for clustering evaluation metrics.

    Attributes:
        calinski_harabasz: Calinski-Harabasz index (higher is better).
        davies_bouldin: Davies-Bouldin index (lower is better).
        silhouette: Silhouette score (higher is better).
        adjusted_rand_index: Adjusted Rand Index (higher is better).
    """

    calinski_harabasz: float
    davies_bouldin: float
    silhouette: float
    adjusted_rand_index: float


class MetricsEvaluator:
    """Evaluates clustering quality using four metrics.

    Metrics computed:
        - Calinski-Harabasz Index
        - Davies-Bouldin Index
        - Silhouette Score (sampled)
        - Adjusted Rand Index (requires true labels)
    """

    def __init__(self, silhouette_sample_size: int = 2000, seed: int = 42) -> None:
        """Initialize MetricsEvaluator.

        Args:
            silhouette_sample_size: Number of samples for silhouette computation.
            seed: Random seed for silhouette sampling.
        """
        self._sample_size = silhouette_sample_size
        self._seed = seed
        logger.info(
            f"MetricsEvaluator initialized — silhouette_sample_size={silhouette_sample_size}"
        )

    def evaluate(
        self, X: np.ndarray, labels: np.ndarray, y_true: np.ndarray
    ) -> MetricsResult:
        """Compute all four clustering metrics.

        Args:
            X: Feature data of shape (N, D).
            labels: Predicted cluster labels of shape (N,).
            y_true: Ground-truth class labels of shape (N,).

        Returns:
            MetricsResult with all four metrics.
        """
        unique_labels = set(labels)
        unique_labels.discard(-1)
        n_clusters = len(unique_labels)

        if n_clusters < 2:
            logger.warning(
                f"Only {n_clusters} cluster(s) found — metrics may be undefined. "
                "Returning default values."
            )
            return MetricsResult(
                calinski_harabasz=0.0,
                davies_bouldin=float("inf"),
                silhouette=-1.0,
                adjusted_rand_index=0.0,
            )

        # Filter out noise points (label == -1) for internal metrics
        mask = labels != -1
        X_valid = X[mask]
        labels_valid = labels[mask]
        y_true_valid = y_true[mask]

        ch = calinski_harabasz_score(X_valid, labels_valid)
        db = davies_bouldin_score(X_valid, labels_valid)

        sil_size = min(self._sample_size, len(X_valid))
        sil = silhouette_score(
            X_valid, labels_valid,
            sample_size=sil_size, random_state=self._seed,
        )

        ari = adjusted_rand_score(y_true_valid, labels_valid)

        result = MetricsResult(
            calinski_harabasz=ch,
            davies_bouldin=db,
            silhouette=sil,
            adjusted_rand_index=ari,
        )
        logger.info(
            f"Metrics — CH: {ch:.2f}, DB: {db:.4f}, Sil: {sil:.4f}, ARI: {ari:.4f}"
        )
        return result
