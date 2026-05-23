"""Tests for SHAPAnalyzer — verifies it never raises and creates output files."""

from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np
import pytest
from sklearn.ensemble import RandomForestRegressor

from diabetes_reg.explainability.shap_analyzer import SHAPAnalyzer


FEATURE_NAMES = ["age", "sex", "bmi", "bp", "s1", "s2", "s3", "s4", "s5", "s6"]
N_TRAIN = 60
N_TEST = 20
N_FEATURES = 10
RANDOM_STATE = 42


@pytest.fixture(scope="module")
def sample_data() -> tuple:
    """Generate small synthetic train/test arrays for SHAP tests."""
    rng = np.random.default_rng(RANDOM_STATE)
    X_train = rng.random((N_TRAIN, N_FEATURES)).astype(np.float32)
    y_train = rng.random(N_TRAIN).astype(np.float32)
    X_test = rng.random((N_TEST, N_FEATURES)).astype(np.float32)
    return X_train, y_train, X_test


@pytest.fixture(scope="module")
def fitted_rf(sample_data: tuple) -> RandomForestRegressor:
    """Return a small Random Forest fitted on the synthetic data."""
    X_train, y_train, _ = sample_data
    model = RandomForestRegressor(n_estimators=5, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    return model


class TestSHAPAnalyzer:
    """Tests for the SHAPAnalyzer class."""

    def test_shap_does_not_raise(
        self, sample_data: tuple, fitted_rf: RandomForestRegressor
    ) -> None:
        """SHAPAnalyzer.analyze() must never raise regardless of model or data."""
        X_train, _, X_test = sample_data
        with tempfile.TemporaryDirectory() as tmp_dir:
            analyzer = SHAPAnalyzer(
                feature_names=FEATURE_NAMES,
                figures_dir=tmp_dir,
                random_state=RANDOM_STATE,
            )
            # Should complete without any exception
            analyzer.analyze(fitted_rf, X_train, X_test, "Random Forest", fold=0)

    def test_output_files_created(
        self, sample_data: tuple, fitted_rf: RandomForestRegressor
    ) -> None:
        """A SHAP summary PNG must exist after analyze() for a tree model."""
        X_train, _, X_test = sample_data
        with tempfile.TemporaryDirectory() as tmp_dir:
            analyzer = SHAPAnalyzer(
                feature_names=FEATURE_NAMES,
                figures_dir=tmp_dir,
                random_state=RANDOM_STATE,
            )
            analyzer.analyze(fitted_rf, X_train, X_test, "Random Forest", fold=0)

            shap_dir = Path(tmp_dir) / "shap"
            summary_file = shap_dir / "shap_summary_fold1_Random_Forest.png"
            assert summary_file.exists(), (
                f"Expected SHAP summary file not found: {summary_file}"
            )

    def test_shap_does_not_raise_on_bad_model(self, sample_data: tuple) -> None:
        """analyze() must not raise even if the model is incompatible with SHAP."""

        class BrokenModel:
            """Dummy model whose predict method always raises."""

            def predict(self, X: np.ndarray) -> np.ndarray:
                raise RuntimeError("Intentional failure for testing.")

        X_train, _, X_test = sample_data
        with tempfile.TemporaryDirectory() as tmp_dir:
            analyzer = SHAPAnalyzer(
                feature_names=FEATURE_NAMES,
                figures_dir=tmp_dir,
                random_state=RANDOM_STATE,
            )
            # Must not propagate the RuntimeError
            analyzer.analyze(BrokenModel(), X_train, X_test, "Broken Model", fold=0)
