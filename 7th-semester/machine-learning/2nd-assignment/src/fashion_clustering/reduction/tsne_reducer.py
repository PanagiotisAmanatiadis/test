"""t-SNE dimensionality reduction."""

from __future__ import annotations

import numpy as np
from loguru import logger
from sklearn.manifold import TSNE

from .base import AbstractReducer


class TSNEReducer(AbstractReducer):
    """t-Distributed Stochastic Neighbor Embedding reducer.

    Note: t-SNE does not support a separate transform step, so fit and
    transform are combined. The fitted embedding is cached for reuse.
    """

    def __init__(
        self,
        n_components: int = 2,
        perplexity: float = 30.0,
        seed: int = 42,
    ) -> None:
        """Initialize TSNEReducer.

        Args:
            n_components: Target dimensionality (typically 2).
            perplexity: Perplexity parameter.
            seed: Random seed.
        """
        self._n_components = n_components
        self._perplexity = perplexity
        self._seed = seed
        self._tsne = TSNE(
            n_components=n_components,
            perplexity=perplexity,
            random_state=seed,
            init="pca",
            learning_rate="auto",
        )
        self._train_embedding: np.ndarray | None = None
        self._X_train_ref: np.ndarray | None = None
        logger.info(
            f"TSNEReducer initialized — n_components={n_components}, perplexity={perplexity}"
        )

    def fit(self, X_train: np.ndarray, X_val: np.ndarray | None = None) -> TSNEReducer:
        """Fit t-SNE on training data (computes embedding immediately).

        Args:
            X_train: Training data of shape (N, D).
            X_val: Ignored for t-SNE.

        Returns:
            Self.
        """
        logger.info(f"Fitting t-SNE on data with shape {X_train.shape}")
        self._train_embedding = self._tsne.fit_transform(X_train)
        self._X_train_ref = X_train
        logger.info("t-SNE fit complete")
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Transform data using t-SNE.

        Since t-SNE has no out-of-sample transform, this re-fits on the
        provided data if it differs from the training data.

        Args:
            X: Data of shape (N, D).

        Returns:
            Embedded data of shape (N, n_components).
        """
        if (
            self._X_train_ref is not None
            and X.shape == self._X_train_ref.shape
            and np.array_equal(X, self._X_train_ref)
        ):
            logger.debug("Returning cached t-SNE training embedding")
            return self._train_embedding

        logger.info(f"Re-fitting t-SNE for new data with shape {X.shape}")
        tsne = TSNE(
            n_components=self._n_components,
            perplexity=self._perplexity,
            random_state=self._seed,
            init="pca",
            learning_rate="auto",
        )
        Z = tsne.fit_transform(X)
        logger.debug(f"t-SNE transform: {X.shape} -> {Z.shape}")
        return Z

    @property
    def name(self) -> str:
        """Human-readable name."""
        return "t-SNE"
