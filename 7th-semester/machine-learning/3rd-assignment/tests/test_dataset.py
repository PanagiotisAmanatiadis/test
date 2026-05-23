"""Tests for DiabetesDataset loading, validation, and normalization."""

from __future__ import annotations

import numpy as np
import pytest
from omegaconf import OmegaConf

from diabetes_reg.data.dataset import DiabetesDataset


@pytest.fixture(scope="module")
def dataset() -> DiabetesDataset:
    """Load, check, and normalize the dataset once for all tests in this module."""
    cfg = OmegaConf.create({"seed": 42})
    ds = DiabetesDataset(cfg)
    ds.load()
    ds.check_nan()
    ds.normalize()
    return ds


class TestDiabetesDataset:
    """Tests for the DiabetesDataset class."""

    def test_load_shape(self, dataset: DiabetesDataset) -> None:
        """Dataset must have 442 samples and 11 columns (10 features + target)."""
        assert dataset.df.shape[0] == 442
        assert dataset.df.shape[1] == 11

    def test_no_nan(self, dataset: DiabetesDataset) -> None:
        """No NaN values should be present after load and check_nan."""
        assert dataset.df.isnull().sum().sum() == 0

    def test_normalization_range(self, dataset: DiabetesDataset) -> None:
        """Both X and y must be fully within [0, 1] after normalize."""
        assert float(dataset.X.min()) >= 0.0
        assert float(dataset.X.max()) <= 1.0
        assert float(dataset.y.min()) >= 0.0
        assert float(dataset.y.max()) <= 1.0

    def test_feature_count(self, dataset: DiabetesDataset) -> None:
        """There must be exactly 10 feature names."""
        assert len(dataset.feature_names) == 10

    def test_denormalize_roundtrip(self, dataset: DiabetesDataset) -> None:
        """denormalize_y(y_normalized) must recover the original target values."""
        y_original = dataset.df["target"].values
        y_recovered = dataset.denormalize_y(dataset.y)
        np.testing.assert_allclose(y_original, y_recovered, rtol=1e-5)
