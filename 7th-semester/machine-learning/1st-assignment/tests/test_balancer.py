"""Tests for RandomUnderSampler."""

from __future__ import annotations

import numpy as np
import pytest

from bankruptcy_clf.preprocessing.balancer import RandomUnderSampler


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_imbalanced(
    n_healthy: int = 120, n_bankrupt: int = 20, seed: int = 0
) -> tuple[np.ndarray, np.ndarray]:
    """Create a synthetic imbalanced dataset with 2 features."""
    rng = np.random.default_rng(seed)
    X_healthy = rng.normal(loc=0.0, scale=1.0, size=(n_healthy, 2))
    X_bankrupt = rng.normal(loc=1.0, scale=1.0, size=(n_bankrupt, 2))
    X = np.vstack([X_healthy, X_bankrupt])
    y = np.concatenate([np.zeros(n_healthy, dtype=int), np.ones(n_bankrupt, dtype=int)])
    return X, y


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestRandomUnderSampler:
    """Tests for RandomUnderSampler.balance()."""

    def test_ratio_enforced(self) -> None:
        """After balancing, the healthy-to-bankrupt ratio must be exactly 3:1."""
        X, y = _make_imbalanced(n_healthy=120, n_bankrupt=20)
        sampler = RandomUnderSampler(target_ratio=3, random_state=42)
        X_bal, y_bal, was_balanced = sampler.balance(X, y, fold_idx=0)

        n_healthy_after = int((y_bal == 0).sum())
        n_bankrupt_after = int((y_bal == 1).sum())

        assert was_balanced is True, "Expected was_balanced=True for 6:1 input ratio."
        assert n_bankrupt_after == 20, "Bankrupt count must not change."
        assert n_healthy_after == 60, (
            f"Expected 60 healthy samples (3 * 20), got {n_healthy_after}."
        )
        assert n_healthy_after / n_bankrupt_after == 3.0

    def test_no_data_added_to_test(self) -> None:
        """balance() must only reduce samples — it must never add samples."""
        X, y = _make_imbalanced(n_healthy=90, n_bankrupt=10)
        original_total = len(X)
        sampler = RandomUnderSampler(target_ratio=3, random_state=42)
        X_bal, y_bal, _ = sampler.balance(X, y, fold_idx=1)

        # The balanced set must be strictly smaller than the original
        assert len(X_bal) <= original_total, (
            "balance() must not increase the total number of samples."
        )
        assert len(X_bal) == len(y_bal), "X and y lengths must match after balancing."

    def test_no_balance_needed(self) -> None:
        """When ratio <= target_ratio, original data must be returned unchanged."""
        # Natural ratio is 2:1 which is <= target_ratio 3
        X, y = _make_imbalanced(n_healthy=40, n_bankrupt=20)
        sampler = RandomUnderSampler(target_ratio=3, random_state=42)
        X_bal, y_bal, was_balanced = sampler.balance(X, y, fold_idx=0)

        assert was_balanced is False, "Expected was_balanced=False when ratio <= 3."
        assert len(X_bal) == len(X), "Data must be unchanged when no balancing is needed."
        np.testing.assert_array_equal(X_bal, X)
        np.testing.assert_array_equal(y_bal, y)

    def test_reproducibility(self) -> None:
        """Two calls with the same seed and fold_idx must yield identical results."""
        X, y = _make_imbalanced(n_healthy=120, n_bankrupt=20)
        sampler = RandomUnderSampler(target_ratio=3, random_state=99)

        X1, y1, _ = sampler.balance(X, y, fold_idx=2)
        X2, y2, _ = sampler.balance(X, y, fold_idx=2)

        np.testing.assert_array_equal(X1, X2)
        np.testing.assert_array_equal(y1, y2)

    def test_different_folds_differ(self) -> None:
        """Different fold indices must produce different (but valid) samples."""
        X, y = _make_imbalanced(n_healthy=120, n_bankrupt=20)
        sampler = RandomUnderSampler(target_ratio=3, random_state=42)

        X0, _, _ = sampler.balance(X, y, fold_idx=0)
        X1, _, _ = sampler.balance(X, y, fold_idx=1)

        # With different seeds the selected healthy rows should differ
        assert not np.array_equal(X0, X1), (
            "Different fold indices should produce different sample selections."
        )
