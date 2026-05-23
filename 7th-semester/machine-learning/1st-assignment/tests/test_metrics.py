"""Tests for MetricsEvaluator and ClassificationResult."""

from __future__ import annotations

import numpy as np
import pytest

from bankruptcy_clf.evaluation.metrics import ClassificationResult, MetricsEvaluator


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def evaluator() -> MetricsEvaluator:
    """Single MetricsEvaluator instance shared across all tests in this module."""
    return MetricsEvaluator()


def _call_evaluate(
    evaluator: MetricsEvaluator,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_prob: np.ndarray,
    *,
    classifier_name: str = "TestCLF",
    split: str = "Test",
    balance_label: str = "Balanced",
    fold: int = 1,
    n_train_samples: int = 100,
    n_train_bankrupt: int = 25,
) -> ClassificationResult:
    """Thin wrapper so tests can call evaluate() without repeating metadata."""
    return evaluator.evaluate(
        y_true=y_true,
        y_pred=y_pred,
        y_prob=y_prob,
        classifier_name=classifier_name,
        split=split,
        balance_label=balance_label,
        fold=fold,
        n_train_samples=n_train_samples,
        n_train_bankrupt=n_train_bankrupt,
    )


def _make_result(
    tp: int = 10, tn: int = 20, fp: int = 5, fn: int = 3
) -> ClassificationResult:
    """Build a ClassificationResult with explicit confusion-matrix counts."""
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
    return ClassificationResult(
        classifier_name="TestCLF",
        split="Test",
        balance_label="Balanced",
        fold=1,
        n_train_samples=100,
        n_train_bankrupt=25,
        tp=tp,
        tn=tn,
        fp=fp,
        fn=fn,
        roc_auc=0.88,
        accuracy=accuracy,
        precision=precision,
        recall=recall,
        f1=f1,
        specificity=specificity,
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestMetricsEvaluator:
    """Tests for MetricsEvaluator.evaluate() and results_to_dataframe()."""

    def test_perfect_predictions(self, evaluator: MetricsEvaluator) -> None:
        """All metrics must equal 1.0 for a perfect classifier."""
        y_true = np.array([0] * 30 + [1] * 30)
        y_pred = y_true.copy()
        y_prob = y_true.astype(float)

        result = _call_evaluate(evaluator, y_true, y_pred, y_prob)

        assert isinstance(result, ClassificationResult)
        assert result.accuracy == pytest.approx(1.0), "Perfect accuracy expected."
        assert result.precision == pytest.approx(1.0), "Perfect precision expected."
        assert result.recall == pytest.approx(1.0), "Perfect recall expected."
        assert result.f1 == pytest.approx(1.0), "Perfect F1 expected."
        assert result.specificity == pytest.approx(1.0), "Perfect specificity expected."
        assert result.roc_auc == pytest.approx(1.0), "Perfect AUC expected."

    def test_specificity_formula(self, evaluator: MetricsEvaluator) -> None:
        """Specificity must equal TN / (TN + FP)."""
        # TN=8, FP=2 => specificity = 8/10 = 0.8
        y_true = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1])
        y_pred = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1])
        y_prob = y_pred.astype(float)

        result = _call_evaluate(evaluator, y_true, y_pred, y_prob)

        expected_specificity = result.tn / (result.tn + result.fp)
        assert result.specificity == pytest.approx(expected_specificity, abs=1e-4), (
            f"Specificity should be TN/(TN+FP) = {expected_specificity:.4f}, "
            f"got {result.specificity:.4f}"
        )

    def test_results_to_dataframe(self, evaluator: MetricsEvaluator) -> None:
        """results_to_dataframe must produce a DataFrame with the correct columns."""
        r1 = _make_result(tp=10, tn=20, fp=5, fn=3)
        r2 = _make_result(tp=15, tn=18, fp=3, fn=2)
        df = evaluator.results_to_dataframe([r1, r2])

        expected_columns = {
            "Classifier Name",
            "Training or Test Set",
            "Balanced or Unbalanced",
            "Fold",
            "Number of Training Samples",
            "Number of Non-Healthy Companies",
            "True Positives (TP)",
            "True Negatives (TN)",
            "False Positives (FP)",
            "False Negatives (FN)",
            "ROC-AUC",
            "Accuracy",
            "Precision",
            "Recall",
            "F1 Score",
            "Specificity",
        }
        assert set(df.columns) == expected_columns, (
            f"Column mismatch. Missing: {expected_columns - set(df.columns)}, "
            f"Extra: {set(df.columns) - expected_columns}"
        )
        assert len(df) == 2, "DataFrame should contain one row per result."

    def test_confusion_matrix_counts(self, evaluator: MetricsEvaluator) -> None:
        """TP + TN + FP + FN must equal the total number of evaluated samples."""
        y_true = np.array([0, 0, 1, 1, 0, 1, 0, 1])
        y_pred = np.array([0, 1, 1, 0, 0, 1, 1, 0])
        y_prob = y_pred.astype(float)

        result = _call_evaluate(evaluator, y_true, y_pred, y_prob)
        total = result.tp + result.tn + result.fp + result.fn

        assert total == len(y_true), (
            f"TP+TN+FP+FN={total} does not equal n_samples={len(y_true)}."
        )

    def test_zero_division_safe(self, evaluator: MetricsEvaluator) -> None:
        """Metrics must not raise when all predictions are the same class."""
        y_true = np.array([0, 0, 1, 1, 1])
        y_pred = np.array([0, 0, 0, 0, 0])  # All predicted healthy
        y_prob = np.zeros(5, dtype=float)

        result = _call_evaluate(evaluator, y_true, y_pred, y_prob)

        assert result.precision == 0.0
        assert result.recall == 0.0
        assert result.f1 == 0.0

    def test_result_metadata_preserved(self, evaluator: MetricsEvaluator) -> None:
        """Metadata passed to evaluate() must appear unchanged in the result."""
        y_true = np.array([0, 0, 1, 1])
        y_pred = np.array([0, 1, 1, 0])
        y_prob = y_pred.astype(float)

        result = _call_evaluate(
            evaluator,
            y_true,
            y_pred,
            y_prob,
            classifier_name="Random Forest",
            split="Train",
            balance_label="Unbalanced",
            fold=3,
            n_train_samples=200,
            n_train_bankrupt=50,
        )

        assert result.classifier_name == "Random Forest"
        assert result.split == "Train"
        assert result.balance_label == "Unbalanced"
        assert result.fold == 3
        assert result.n_train_samples == 200
        assert result.n_train_bankrupt == 50
