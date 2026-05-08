"""Evaluation metrics for the recommendation system."""

import logging
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

from recommender.models.base import BaseRecommender

logger = logging.getLogger(__name__)

_POSITIVE_THRESHOLD = 3.5  # ratings >= this are considered "liked"


@dataclass
class EvalResult:
    """Aggregate evaluation metrics for one model run."""

    model_name:  str
    mae:         float
    rmse:        float
    precision:   float
    recall:      float
    f1:          float
    coverage:    float          # fraction of test pairs that could be predicted
    n_predicted: int
    n_total:     int
    extra:       dict = field(default_factory=dict)

    def __str__(self) -> str:
        lines = [
            f"Model      : {self.model_name}",
            f"Coverage   : {self.coverage:.1%}  ({self.n_predicted}/{self.n_total} predictions)",
            f"MAE        : {self.mae:.4f}",
            f"RMSE       : {self.rmse:.4f}",
            f"Precision  : {self.precision:.4f}",
            f"Recall     : {self.recall:.4f}",
            f"F1         : {self.f1:.4f}",
        ]
        return "\n".join(lines)


class Evaluator:
    """Runs a model against a test set and computes evaluation metrics.

    Metrics
    -------
    MAE     — Mean Absolute Error on predicted vs actual ratings.
    RMSE    — Root Mean Squared Error.
    Precision — fraction of predicted-positive items that are truly positive.
    Recall    — fraction of truly-positive items that were predicted positive.
    F1        — harmonic mean of precision and recall.
    Coverage  — percentage of test entries for which a prediction was possible.
    """

    def evaluate(
        self,
        model:      BaseRecommender,
        test:       pd.DataFrame,
        model_name: str = "model",
    ) -> EvalResult:
        """Generate predictions and compute all metrics.

        Args:
            model:      A fitted :class:`~recommender.models.base.BaseRecommender`.
            test:       Test DataFrame with [userId, movieId, rating].
            model_name: Label used in the returned :class:`EvalResult`.

        Returns:
            :class:`EvalResult` with all computed metrics.
        """
        logger.info("Evaluating %s on %d test pairs …", model_name, len(test))

        predictions = model.predict_batch(test)
        actuals     = test["rating"].to_numpy(dtype=np.float32)

        valid_mask  = ~np.isnan(predictions)
        n_predicted = int(valid_mask.sum())
        coverage    = n_predicted / len(test) if len(test) > 0 else 0.0

        if n_predicted == 0:
            logger.warning("No predictions could be made — cannot compute metrics.")
            return EvalResult(
                model_name=model_name, mae=np.nan, rmse=np.nan,
                precision=np.nan, recall=np.nan, f1=np.nan,
                coverage=0.0, n_predicted=0, n_total=len(test),
            )

        pred_valid   = predictions[valid_mask]
        actual_valid = actuals[valid_mask]

        mae  = float(mean_absolute_error(actual_valid, pred_valid))
        rmse = float(np.sqrt(mean_squared_error(actual_valid, pred_valid)))

        # Binary classification metrics (liked = rating >= threshold)
        pred_positive   = (pred_valid   >= _POSITIVE_THRESHOLD).astype(int)
        actual_positive = (actual_valid >= _POSITIVE_THRESHOLD).astype(int)

        tp = int(((pred_positive == 1) & (actual_positive == 1)).sum())
        fp = int(((pred_positive == 1) & (actual_positive == 0)).sum())
        fn = int(((pred_positive == 0) & (actual_positive == 1)).sum())

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall    = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1        = (
            2 * precision * recall / (precision + recall)
            if (precision + recall) > 0 else 0.0
        )

        result = EvalResult(
            model_name=model_name,
            mae=mae, rmse=rmse,
            precision=precision, recall=recall, f1=f1,
            coverage=coverage,
            n_predicted=n_predicted,
            n_total=len(test),
        )
        logger.info("Results:\n%s", result)
        return result
