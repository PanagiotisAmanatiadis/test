"""Regression evaluation metrics with normalized and original-scale reporting."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np
from loguru import logger
from sklearn.metrics import max_error, mean_absolute_error, mean_squared_error
from sklearn.preprocessing import MinMaxScaler


@dataclass
class RegressionResult:
    """Container for regression evaluation metrics at one fold/split.

    Attributes:
        model_name: Display name of the regression model.
        split: Dataset split label, either "Train" or "Test".
        fold: One-based fold index.
        max_n: Max absolute error in normalized [0, 1] scale.
        rmse_n: RMSE in normalized [0, 1] scale.
        mae_n: MAE in normalized [0, 1] scale.
        mape_n: MAPE in normalized scale (percent).
        max: Max absolute error in original mg/dL scale.
        rmse: RMSE in original mg/dL scale.
        mae: MAE in original mg/dL scale.
        mape: MAPE in original mg/dL scale (percent).
    """

    model_name: str
    split: str
    fold: int
    max_n: float
    rmse_n: float
    mae_n: float
    mape_n: float
    max: float
    rmse: float
    mae: float
    mape: float


class MetricsEvaluator:
    """Computes regression error metrics in both normalized and original scales.

    All metrics are computed from predictions that remain in the normalized
    [0, 1] space; denormalization is applied internally before computing
    original-scale values.
    """

    def evaluate(
        self,
        y_true_norm: np.ndarray,
        y_pred_norm: np.ndarray,
        scaler_y: MinMaxScaler,
    ) -> Tuple[Dict[str, float], Dict[str, float]]:
        """Compute error metrics in both normalized and original scales.

        Args:
            y_true_norm: Ground-truth values in [0, 1] normalized scale.
            y_pred_norm: Predicted values in [0, 1] normalized scale.
            scaler_y: Fitted MinMaxScaler used to invert the target transform.

        Returns:
            Tuple of (normalized_metrics, original_metrics) where each is a
            dict with keys Max_n/RMSE_n/MAE_n/MAPE_n or Max/RMSE/MAE/MAPE.
        """
        y_true_orig = scaler_y.inverse_transform(
            y_true_norm.reshape(-1, 1)
        ).ravel()
        y_pred_orig = scaler_y.inverse_transform(
            y_pred_norm.reshape(-1, 1)
        ).ravel()

        norm_metrics: Dict[str, float] = {
            "Max_n": float(max_error(y_true_norm, y_pred_norm)),
            "RMSE_n": float(np.sqrt(mean_squared_error(y_true_norm, y_pred_norm))),
            "MAE_n": float(mean_absolute_error(y_true_norm, y_pred_norm)),
            "MAPE_n": self._safe_mape(y_true_norm, y_pred_norm),
        }

        orig_metrics: Dict[str, float] = {
            "Max": float(max_error(y_true_orig, y_pred_orig)),
            "RMSE": float(np.sqrt(mean_squared_error(y_true_orig, y_pred_orig))),
            "MAE": float(mean_absolute_error(y_true_orig, y_pred_orig)),
            "MAPE": self._safe_mape(y_true_orig, y_pred_orig),
        }

        return norm_metrics, orig_metrics

    @staticmethod
    def _safe_mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Compute MAPE with zero-division protection.

        Args:
            y_true: Ground-truth values.
            y_pred: Predicted values.

        Returns:
            MAPE as a percentage, or NaN if all true values are zero.
        """
        mask = y_true != 0
        if mask.sum() == 0:
            logger.warning("All true values are zero; MAPE is undefined.")
            return float("nan")
        return float(
            np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100
        )

    @staticmethod
    def results_to_csv_rows(results: List[RegressionResult]) -> List[List]:
        """Convert a list of RegressionResult objects to CSV-ready rows.

        The row order matches the assignment header exactly:
        Model | Set | Fold | Max_n | RMSE_n | MAE_n | MAPE_n | Max | RMSE | MAE | MAPE

        Args:
            results: List of RegressionResult dataclass instances.

        Returns:
            List of lists, one inner list per result record.
        """
        rows: List[List] = []
        for r in results:
            rows.append([
                r.model_name,
                r.split,
                r.fold,
                round(r.max_n, 4),
                round(r.rmse_n, 4),
                round(r.mae_n, 4),
                round(r.mape_n, 4),
                round(r.max, 4),
                round(r.rmse, 4),
                round(r.mae, 4),
                round(r.mape, 4),
            ])
        return rows
