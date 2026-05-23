"""Classification metrics — dataclass result container and evaluator."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List

import numpy as np
import pandas as pd
from loguru import logger
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


@dataclass
class ClassificationResult:
    """Container for a single classifier evaluation record.

    Attributes:
        classifier_name: Display name of the classifier.
        split: "Train" or "Test".
        balance_label: "Balanced" or "Unbalanced".
        fold: 1-based fold index.
        n_train_samples: Total samples in the training set for this fold.
        n_train_bankrupt: Bankrupt (positive) samples in the training set.
        tp: True positives.
        tn: True negatives.
        fp: False positives.
        fn: False negatives.
        roc_auc: Area under the ROC curve.
        accuracy: Overall accuracy.
        precision: Positive predictive value.
        recall: True positive rate (sensitivity).
        f1: Harmonic mean of precision and recall.
        specificity: True negative rate — TN / (TN + FP).
    """

    classifier_name: str
    split: str
    balance_label: str
    fold: int
    n_train_samples: int
    n_train_bankrupt: int
    tp: int
    tn: int
    fp: int
    fn: int
    roc_auc: float
    accuracy: float
    precision: float
    recall: float
    f1: float
    specificity: float


class MetricsEvaluator:
    """Computes all classification metrics for a single prediction batch."""

    def evaluate(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_prob: np.ndarray,
        classifier_name: str,
        split: str,
        balance_label: str,
        fold: int,
        n_train_samples: int,
        n_train_bankrupt: int,
    ) -> ClassificationResult:
        """Compute metrics and package them into a ClassificationResult.

        Args:
            y_true: Ground-truth binary labels (0=healthy, 1=bankrupt).
            y_pred: Predicted binary labels.
            y_prob: Predicted probabilities for the positive class.
            classifier_name: Display name of the classifier.
            split: "Train" or "Test".
            balance_label: "Balanced" or "Unbalanced".
            fold: 1-based fold index.
            n_train_samples: Training set size for this fold.
            n_train_bankrupt: Bankrupt count in training set.

        Returns:
            Populated ClassificationResult dataclass instance.
        """
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()

        accuracy  = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, zero_division=0)
        recall    = recall_score(y_true, y_pred, zero_division=0)
        f1        = f1_score(y_true, y_pred, zero_division=0)

        try:
            auc = roc_auc_score(y_true, y_prob)
        except Exception:
            auc = float("nan")

        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0

        logger.info(
            f"    {split:5s} | Acc={accuracy:.2f}  Prec={precision:.2f}  "
            f"Rec={recall:.2f}  F1={f1:.2f}  AUC={auc:.2f}  Spec={specificity:.2f}"
        )

        return ClassificationResult(
            classifier_name=classifier_name,
            split=split,
            balance_label=balance_label,
            fold=fold,
            n_train_samples=n_train_samples,
            n_train_bankrupt=n_train_bankrupt,
            tp=int(tp),
            tn=int(tn),
            fp=int(fp),
            fn=int(fn),
            roc_auc=round(auc, 4),
            accuracy=round(accuracy, 4),
            precision=round(precision, 4),
            recall=round(recall, 4),
            f1=round(f1, 4),
            specificity=round(specificity, 4),
        )

    @staticmethod
    def results_to_dataframe(results: List[ClassificationResult]) -> pd.DataFrame:
        """Convert a list of ClassificationResult instances to a DataFrame.

        Args:
            results: List of ClassificationResult instances.

        Returns:
            DataFrame with assignment-specification column names.
        """
        records = []
        for r in results:
            records.append({
                "Classifier Name":                r.classifier_name,
                "Training or Test Set":           r.split,
                "Balanced or Unbalanced":         r.balance_label,
                "Fold":                           r.fold,
                "Number of Training Samples":     r.n_train_samples,
                "Number of Non-Healthy Companies":r.n_train_bankrupt,
                "True Positives (TP)":            r.tp,
                "True Negatives (TN)":            r.tn,
                "False Positives (FP)":           r.fp,
                "False Negatives (FN)":           r.fn,
                "ROC-AUC":                        r.roc_auc,
                "Accuracy":                       r.accuracy,
                "Precision":                      r.precision,
                "Recall":                         r.recall,
                "F1 Score":                       r.f1,
                "Specificity":                    r.specificity,
            })
        return pd.DataFrame(records)
