"""Tests for FashionMNISTDataset."""

import numpy as np
import pytest

from fashion_clustering.data.dataset import FashionMNISTDataset, CLASS_NAMES


@pytest.fixture(scope="module")
def dataset() -> FashionMNISTDataset:
    """Load dataset once for all tests in this module."""
    return FashionMNISTDataset(val_split=0.1666, seed=42)


class TestFashionMNISTDataset:
    """Tests for the FashionMNISTDataset class."""

    def test_shapes(self, dataset: FashionMNISTDataset) -> None:
        """Verify expected shapes after loading."""
        assert dataset.X_train.ndim == 2
        assert dataset.X_train.shape[1] == 784
        assert dataset.X_test.shape == (10000, 784)
        assert dataset.X_val.ndim == 2

    def test_normalization(self, dataset: FashionMNISTDataset) -> None:
        """Pixel values should be in [0, 1]."""
        assert dataset.X_train.min() >= 0.0
        assert dataset.X_train.max() <= 1.0
        assert dataset.X_test.min() >= 0.0
        assert dataset.X_test.max() <= 1.0

    def test_labels(self, dataset: FashionMNISTDataset) -> None:
        """Labels should be 0-9."""
        assert set(np.unique(dataset.y_train)) == set(range(10))
        assert set(np.unique(dataset.y_test)) == set(range(10))

    def test_2d_shapes(self, dataset: FashionMNISTDataset) -> None:
        """2D images should have shape (N, 28, 28, 1)."""
        assert dataset.X_train_2d.shape[1:] == (28, 28, 1)
        assert dataset.X_test_2d.shape == (10000, 28, 28, 1)

    def test_class_names(self) -> None:
        """There should be 10 class names."""
        assert len(CLASS_NAMES) == 10
