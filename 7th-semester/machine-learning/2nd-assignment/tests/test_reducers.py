"""Tests for dimensionality reduction strategies."""

import numpy as np
import pytest

from fashion_clustering.reduction.factory import ReductionFactory
from fashion_clustering.reduction.base import AbstractReducer


@pytest.fixture
def small_data() -> tuple[np.ndarray, np.ndarray]:
    """Create small synthetic data for fast testing."""
    rng = np.random.RandomState(42)
    X_train = rng.rand(200, 784).astype(np.float32)
    X_val = rng.rand(50, 784).astype(np.float32)
    return X_train, X_val


class TestPCAReducer:
    """Tests for PCAReducer."""

    def test_factory_creation(self) -> None:
        """PCA reducer can be created via factory."""
        reducer = ReductionFactory.create("pca", n_components=10)
        assert isinstance(reducer, AbstractReducer)
        assert reducer.name == "PCA"

    def test_fit_transform(self, small_data: tuple) -> None:
        """PCA fit and transform produce expected shapes."""
        X_train, _ = small_data
        reducer = ReductionFactory.create("pca", n_components=10)
        reducer.fit(X_train)
        Z = reducer.transform(X_train)
        assert Z.shape == (200, 10)

    def test_reconstruct(self, small_data: tuple) -> None:
        """PCA can reconstruct data."""
        X_train, _ = small_data
        reducer = ReductionFactory.create("pca", n_components=10)
        reducer.fit(X_train)
        X_recon = reducer.reconstruct(X_train)
        assert X_recon is not None
        assert X_recon.shape == X_train.shape


class TestSAEReducer:
    """Tests for SAEReducer."""

    def test_factory_creation(self) -> None:
        """SAE reducer can be created via factory."""
        reducer = ReductionFactory.create(
            "sae", layers=[64, 32], latent_dim=8, epochs=1, batch_size=32,
        )
        assert reducer.name == "SAE"

    def test_fit_transform(self, small_data: tuple) -> None:
        """SAE fit and transform produce expected shapes."""
        X_train, X_val = small_data
        reducer = ReductionFactory.create(
            "sae", layers=[64, 32], latent_dim=8, epochs=1, batch_size=32,
        )
        reducer.fit(X_train, X_val)
        Z = reducer.transform(X_train)
        assert Z.shape == (200, 8)


class TestFactoryErrors:
    """Tests for factory error handling."""

    def test_unknown_reducer(self) -> None:
        """Unknown key should raise ValueError."""
        with pytest.raises(ValueError, match="Unknown reducer"):
            ReductionFactory.create("nonexistent")
