"""Random undersampling for class-imbalanced training sets."""
from __future__ import annotations

from typing import Tuple

import numpy as np
from loguru import logger


class RandomUnderSampler:
    """Reduces the majority (healthy) class to a target ratio.

    The removed samples are discarded — they are NOT transferred to the
    test set.  This preserves test-set integrity across all folds.

    Attributes:
        target_ratio: Desired healthy-to-bankrupt ratio (default 3).
        random_state: Base random seed (fold index is added for variety).
    """

    def __init__(self, target_ratio: int = 3, random_state: int = 42) -> None:
        """Initialise RandomUnderSampler.

        Args:
            target_ratio: Healthy-to-bankrupt ratio to enforce.
            random_state: Base seed for reproducible sampling.
        """
        self.target_ratio = target_ratio
        self.random_state = random_state

    def balance(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        fold_idx: int = 0,
    ) -> Tuple[np.ndarray, np.ndarray, bool]:
        """Undersample the majority class if the ratio exceeds target_ratio.

        Args:
            X_train: Training features for this fold.
            y_train: Training labels (0 = healthy, 1 = bankrupt).
            fold_idx: Current fold index (added to seed for variety).

        Returns:
            Tuple of (X_balanced, y_balanced, was_balanced).
            was_balanced is True when undersampling was applied.
        """
        n_healthy = int((y_train == 0).sum())
        n_bankrupt = int((y_train == 1).sum())

        logger.info(
            f"  [BEFORE] TRAIN  Healthy={n_healthy}  Bankrupt={n_bankrupt}"
        )

        ratio = n_healthy / n_bankrupt if n_bankrupt > 0 else 0.0

        if ratio <= self.target_ratio:
            logger.info(
                f"  Ratio {ratio:.2f}:1 ≤ {self.target_ratio}:1 — no undersampling."
            )
            return X_train, y_train, False

        target_n_healthy = self.target_ratio * n_bankrupt

        h_mask = y_train == 0
        X_h, y_h = X_train[h_mask], y_train[h_mask]
        X_b, y_b = X_train[~h_mask], y_train[~h_mask]

        rng = np.random.RandomState(self.random_state + fold_idx)
        chosen = rng.choice(len(X_h), size=target_n_healthy, replace=False)

        X_bal = np.vstack([X_h[chosen], X_b])
        y_bal = np.concatenate([y_h[chosen], y_b])

        perm = rng.permutation(len(X_bal))
        X_bal, y_bal = X_bal[perm], y_bal[perm]

        n_h_bal = int((y_bal == 0).sum())
        n_b_bal = int((y_bal == 1).sum())
        logger.info(
            f"  [AFTER ] TRAIN  Healthy={n_h_bal}  Bankrupt={n_b_bal}  "
            f"(ratio={n_h_bal / n_b_bal:.2f}:1)"
        )
        return X_bal, y_bal, True
