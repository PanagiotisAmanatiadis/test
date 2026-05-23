"""Tests for BankruptcyDataset."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from omegaconf import OmegaConf

from bankruptcy_clf.data.dataset import BankruptcyDataset


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_cfg() -> object:
    """Return a minimal OmegaConf config (no real file needed for unit tests)."""
    return OmegaConf.create({"data": {"path": "data/dummy.xlsx"}, "seed": 42})


def _make_raw_df() -> pd.DataFrame:
    """Build a small synthetic DataFrame that mimics the Excel dataset schema.

    Columns:
        Year    — fiscal year (2015..2018), triggers year-column detection.
        Ind1    — continuous numeric indicator.
        Ind2    — continuous numeric indicator.
        Status  — binary {1=healthy, 2=bankrupt}.
    """
    rng = np.random.default_rng(0)
    n = 40
    return pd.DataFrame(
        {
            "Year": rng.integers(2015, 2019, size=n).astype(float),
            "Ind1": rng.uniform(0.0, 5.0, size=n),
            "Ind2": rng.uniform(-1.0, 1.0, size=n),
            "Status": rng.choice([1, 2], size=n).astype(float),
        }
    )


@pytest.fixture(scope="module")
def dataset() -> BankruptcyDataset:
    """Return a BankruptcyDataset populated with a synthetic in-memory DataFrame."""
    cfg = _make_cfg()
    ds = BankruptcyDataset(cfg)
    ds.df_raw = _make_raw_df()
    ds.normalize()
    return ds


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestBankruptcyDataset:
    """Tests for the BankruptcyDataset class."""

    def test_columns_identified(self, dataset: BankruptcyDataset) -> None:
        """Year column and status column must be auto-detected correctly."""
        assert dataset.year_col == "Year", (
            f"Expected year_col='Year', got '{dataset.year_col}'"
        )
        assert dataset.status_col == "Status", (
            f"Expected status_col='Status', got '{dataset.status_col}'"
        )
        assert "Ind1" in dataset.feature_names
        assert "Ind2" in dataset.feature_names
        # Year and Status must not appear in features
        assert "Year" not in dataset.feature_names
        assert "Status" not in dataset.feature_names

    def test_normalization_range(self, dataset: BankruptcyDataset) -> None:
        """All feature values must lie in the closed interval [0, 1]."""
        assert dataset.X.min() >= 0.0, "Minimum feature value below 0."
        assert dataset.X.max() <= 1.0, "Maximum feature value above 1."

    def test_label_encoding(self, dataset: BankruptcyDataset) -> None:
        """Labels must be binary — only 0 (healthy) and 1 (bankrupt)."""
        unique_labels = set(np.unique(dataset.y))
        assert unique_labels.issubset({0, 1}), (
            f"Unexpected label values: {unique_labels}"
        )

    def test_no_nan_after_clean(self) -> None:
        """After check_missing_values(), no NaN must remain in df_raw."""
        raw_df = _make_raw_df()
        raw_df.loc[3, "Ind1"] = float("nan")
        raw_df.loc[7, "Ind2"] = float("nan")

        cfg = _make_cfg()
        ds = BankruptcyDataset(cfg)
        ds.df_raw = raw_df.copy()

        ds.check_missing_values()

        assert not ds.df_raw.isnull().any().any(), (
            "NaN values remain after check_missing_values()."
        )

    def test_feature_count(self, dataset: BankruptcyDataset) -> None:
        """Number of feature column names must equal width of X array."""
        assert len(dataset.feature_names) == dataset.X.shape[1]

    def test_sample_count(self, dataset: BankruptcyDataset) -> None:
        """X and y must have the same number of rows."""
        assert dataset.X.shape[0] == dataset.y.shape[0]
