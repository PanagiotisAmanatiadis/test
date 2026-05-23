"""Tests for MetricsEvaluator and RegressionResult."""

from __future__ import annotations

import math

import numpy as np
import pytest
from sklearn.preprocessing import MinMaxScaler

from diabetes_reg.evaluation.metrics import MetricsEvaluator, RegressionResult


@pytest.fixture(scope="module")
def fitted_scaler() -> MinMaxScaler:
    """Return a MinMaxScaler fitted on a simple range [50, 350] to mimic mg/dL."""
    scaler = MinMaxScaler()
    scaler.fit(np.array([[50.0], [350.0]]))
    return scaler


@pytest.fixture(scope="module")
def evaluator() -> MetricsEvaluator:
    """Return a shared MetricsEvaluator instance."""
    return MetricsEvaluator()


class TestMetricsEvaluator:
    """Tests for the MetricsEvaluator class."""

    def test_perfect_predictions_rmse(
        self, evaluator: MetricsEvaluator, fitted_scaler: MinMaxScaler
    ) -> None:
        """When predictions equal ground truth, RMSE must be 0 in both scales."""
        y = np.linspace(0.0, 1.0, 50)
        norm_m, orig_m = evaluator.evaluate(y, y, fitted_scaler)
        assert norm_m["RMSE_n"] == pytest.approx(0.0, abs=1e-10)
        assert orig_m["RMSE"] == pytest.approx(0.0, abs=1e-8)

    def test_mape_zero_division_safe(
        self, evaluator: MetricsEvaluator, fitted_scaler: MinMaxScaler
    ) -> None:
        """evaluate() must not raise even when y_true_norm contains zeros."""
        y_true = np.array([0.0, 0.0, 0.0])
        y_pred = np.array([0.1, 0.2, 0.3])
        # Should not raise; MAPE_n will be NaN because all true values are zero
        norm_m, _ = evaluator.evaluate(y_true, y_pred, fitted_scaler)
        assert math.isnan(norm_m["MAPE_n"])

    def test_original_scale_rmse(
        self, evaluator: MetricsEvaluator, fitted_scaler: MinMaxScaler
    ) -> None:
        """RMSE in original scale must reflect the denormalized residuals."""
        # Normalized predictions off by 0.1 across all samples
        y_true_norm = np.full(20, 0.5)
        y_pred_norm = np.full(20, 0.6)

        _, orig_m = evaluator.evaluate(y_true_norm, y_pred_norm, fitted_scaler)

        # Expected original-scale error: 0.1 * (350 - 50) = 30 mg/dL
        expected_rmse = 0.1 * (350.0 - 50.0)
        assert orig_m["RMSE"] == pytest.approx(expected_rmse, rel=1e-5)

    def test_results_to_csv_rows_length(self) -> None:
        """results_to_csv_rows must return one row per RegressionResult."""
        results = [
            RegressionResult(
                model_name="Ridge Regression",
                split="Test",
                fold=1,
                max_n=0.1,
                rmse_n=0.05,
                mae_n=0.04,
                mape_n=8.5,
                max=30.0,
                rmse=15.0,
                mae=12.0,
                mape=8.5,
            ),
            RegressionResult(
                model_name="Random Forest",
                split="Train",
                fold=2,
                max_n=0.08,
                rmse_n=0.03,
                mae_n=0.02,
                mape_n=5.1,
                max=24.0,
                rmse=9.0,
                mae=6.0,
                mape=5.1,
            ),
        ]
        rows = MetricsEvaluator.results_to_csv_rows(results)
        assert len(rows) == 2
        # First column of each row is the model name
        assert rows[0][0] == "Ridge Regression"
        assert rows[1][0] == "Random Forest"

    def test_results_to_csv_rows_rounding(self) -> None:
        """Numeric values in csv rows must be rounded to 4 decimal places."""
        result = RegressionResult(
            model_name="Ridge Regression",
            split="Test",
            fold=1,
            max_n=0.123456789,
            rmse_n=0.098765432,
            mae_n=0.076543210,
            mape_n=12.345678,
            max=37.123456,
            rmse=29.876543,
            mae=22.654321,
            mape=12.3456789,
        )
        rows = MetricsEvaluator.results_to_csv_rows([result])
        row = rows[0]
        # Index 3 is Max_n, should be rounded to 4 dp
        assert row[3] == round(0.123456789, 4)
        assert row[4] == round(0.098765432, 4)
