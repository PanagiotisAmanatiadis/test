"""Experiment pipeline orchestrator for the bankruptcy classification assignment."""

from __future__ import annotations

import warnings
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
from loguru import logger
from omegaconf import OmegaConf
from sklearn.model_selection import StratifiedKFold

from ..data.dataset import BankruptcyDataset
from ..preprocessing.balancer import RandomUnderSampler
from ..models.factory import ClassifierFactory
from ..evaluation.metrics import ClassificationResult, MetricsEvaluator
from ..visualization.plotter import Plotter
from ..utils.logger import setup_logger
from ..utils.timer import Timer

warnings.filterwarnings("ignore")


class ExperimentRunner:
    """Orchestrates the full corporate bankruptcy classification pipeline.

    Loads data, generates EDA figures, runs Stratified K-Fold cross-validation
    with random undersampling, evaluates all classifiers, saves confusion
    matrices, and writes the results CSV.

    Attributes:
        _cfg: Top-level OmegaConf config loaded from the YAML file.
    """

    def __init__(self, config_path: str = "configs/config.yaml") -> None:
        """Initialize ExperimentRunner from a YAML config file.

        Args:
            config_path: Path to the OmegaConf YAML configuration file.
        """
        self._cfg = OmegaConf.load(config_path)
        setup_logger(Path(self._cfg.paths.logs_dir))
        logger.info(f"ExperimentRunner initialized from {config_path}")

    def run(self) -> pd.DataFrame:
        """Execute the complete bankruptcy classification pipeline.

        Steps:
            1. Load and clean the Excel dataset.
            2. Auto-detect column roles (features, status, year).
            3. Generate Figure 1 (class distribution by year).
            4. Generate Figure 2 (indicator statistics by class).
            5. Apply Min-Max normalization.
            6. Run Stratified K-Fold CV with random undersampling.
            7. For each fold: train all classifiers, evaluate train + test splits.
            8. Save confusion matrix figures.
            9. Save results DataFrame to CSV.
            10. Print constraint satisfaction summary.

        Returns:
            DataFrame containing all evaluation records.
        """
        cfg = self._cfg

        logger.info("")
        logger.info("=" * 70)
        logger.info("  CORPORATE BANKRUPTCY CLASSIFICATION PIPELINE")
        logger.info("  University of Macedonia | Machine Learning | Assignment 1")
        logger.info("=" * 70)

        # ------------------------------------------------------------------
        # 1. Dataset
        # ------------------------------------------------------------------
        dataset = BankruptcyDataset(cfg)
        dataset.load()
        dataset.check_missing_values()

        # ------------------------------------------------------------------
        # 2. Normalization (also runs _identify_columns internally)
        # ------------------------------------------------------------------
        dataset.normalize()
        feature_cols = dataset.feature_names
        status_col = dataset.status_col
        year_col = dataset.year_col
        X = dataset.X
        y = dataset.y

        # ------------------------------------------------------------------
        # 3. EDA figures (use raw df which is populated after load/clean)
        # ------------------------------------------------------------------
        plotter = Plotter(
            figures_dir=cfg.paths.figures_dir,
            dpi=cfg.visualization.dpi,
        )

        if year_col is not None:
            plotter.plot_class_distribution_by_year(
                df=dataset.df_raw,
                status_col=status_col,
                year_col=year_col,
            )

        plotter.plot_indicator_statistics(
            df=dataset.df_raw,
            feature_cols=feature_cols,
            status_col=status_col,
        )

        # ------------------------------------------------------------------
        # 4. Cross-validation setup
        # ------------------------------------------------------------------
        seed: int = cfg.seed
        n_folds: int = cfg.pipeline.n_folds
        target_ratio: int = cfg.pipeline.target_ratio

        skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=seed)
        classifiers = ClassifierFactory.create_all(cfg)
        balancer = RandomUnderSampler(target_ratio=target_ratio, random_state=seed)
        evaluator = MetricsEvaluator()

        results: List[ClassificationResult] = []

        # ------------------------------------------------------------------
        # 5. Fold loop
        # ------------------------------------------------------------------
        for fold_idx, (train_idx, test_idx) in enumerate(skf.split(X, y)):
            logger.info("")
            logger.info("=" * 70)
            logger.info(f"  FOLD {fold_idx + 1} / {n_folds}")
            logger.info("=" * 70)

            X_train_raw = X[train_idx]
            y_train_raw = y[train_idx]
            X_test = X[test_idx]
            y_test = y[test_idx]

            n_h_test = int((y_test == 0).sum())
            n_b_test = int((y_test == 1).sum())
            logger.info(
                f"  [BEFORE undersampling] TEST   Healthy={n_h_test}  Bankrupt={n_b_test}"
            )

            # Undersample the training fold
            X_train, y_train, was_balanced = balancer.balance(
                X_train_raw, y_train_raw, fold_idx
            )
            balance_label = "Balanced" if was_balanced else "Unbalanced"
            logger.info(
                f"  [AFTER  undersampling] TEST   Healthy={n_h_test}  Bankrupt={n_b_test}"
                "  (unchanged)"
            )

            n_train_total = len(X_train)
            n_train_bankrupt = int((y_train == 1).sum())

            # --------------------------------------------------------------
            # Train and evaluate each classifier
            # --------------------------------------------------------------
            for clf_name, clf in classifiers.items():
                logger.info(f"  Training: {clf_name:<25} ...")

                with Timer() as elapsed:
                    try:
                        clf.fit(X_train, y_train)
                    except Exception as exc:
                        logger.error(f"    Training FAILED for {clf_name}: {exc}")
                        continue
                logger.debug(f"    Fit time: {elapsed():.3f}s")

                for split_name, X_eval, y_eval in [
                    ("Train", X_train, y_train),
                    ("Test", X_test, y_test),
                ]:
                    try:
                        y_pred = clf.predict(X_eval)

                        # Obtain predicted probabilities for AUC-ROC
                        if hasattr(clf, "predict_proba"):
                            y_prob = clf.predict_proba(X_eval)[:, 1]
                        elif hasattr(clf, "decision_function"):
                            df_scores = clf.decision_function(X_eval)
                            lo, hi = df_scores.min(), df_scores.max()
                            y_prob = (df_scores - lo) / (hi - lo + 1e-9)
                        else:
                            y_prob = y_pred.astype(float)

                        result = evaluator.evaluate(
                            y_true=y_eval,
                            y_pred=y_pred,
                            y_prob=y_prob,
                            classifier_name=clf_name,
                            split=split_name,
                            balance_label=balance_label,
                            fold=fold_idx + 1,
                            n_train_samples=n_train_total,
                            n_train_bankrupt=n_train_bankrupt,
                        )

                        # Save confusion matrix figure
                        plotter.plot_confusion_matrix(
                            y_true=y_eval,
                            y_pred=y_pred,
                            clf_name=clf_name,
                            fold=fold_idx,
                            split=split_name,
                            balanced=was_balanced,
                        )

                        results.append(result)

                    except Exception as exc:
                        logger.error(
                            f"    Evaluation FAILED — {clf_name} / {split_name}: {exc}"
                        )

        # ------------------------------------------------------------------
        # 6. Build results DataFrame
        # ------------------------------------------------------------------
        logger.info("")
        logger.info(f"Cross-validation complete. Total records: {len(results)}")

        results_df = evaluator.results_to_dataframe(results)

        # ------------------------------------------------------------------
        # 7. Save CSV
        # ------------------------------------------------------------------
        csv_path = Path(cfg.paths.results_csv)
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        results_df.to_csv(csv_path, index=False)
        logger.info(f"Results saved: {csv_path}")

        # ------------------------------------------------------------------
        # 8. Constraint summary
        # ------------------------------------------------------------------
        self._print_constraint_summary(results_df, n_folds)

        logger.info("")
        logger.info(f"Pipeline complete. All outputs in: {cfg.paths.figures_dir}")
        return results_df

    def _print_constraint_summary(
        self, results_df: pd.DataFrame, n_folds: int
    ) -> None:
        """Print mean test-set performance and flag classifiers meeting constraints.

        Business constraints:
            - Recall >= 60%  (sensitivity to bankruptcy)
            - Specificity >= 70%  (correct identification of healthy companies)

        Args:
            results_df: Full results DataFrame from the CV loop.
            n_folds: Number of folds (for the header line).
        """
        test_df = results_df[results_df["Training or Test Set"] == "Test"]
        if test_df.empty:
            logger.warning("No test results available for constraint summary.")
            return

        mean_metrics = (
            test_df.groupby("Classifier Name")[["F1 Score", "Recall", "Specificity"]]
            .mean()
            .sort_values("F1 Score", ascending=False)
        )

        logger.info("")
        logger.info("-" * 70)
        logger.info(f"  MEAN TEST-SET PERFORMANCE ACROSS {n_folds} FOLDS")
        logger.info("-" * 70)

        for clf_name, row in mean_metrics.iterrows():
            meets_recall = row["Recall"] >= 0.60
            meets_spec = row["Specificity"] >= 0.70
            meets_both = meets_recall and meets_spec
            tag = " <- [MEETS BOTH CONSTRAINTS]" if meets_both else ""
            logger.info(
                f"  {clf_name:<25} F1={row['F1 Score']:.4f}"
                f"  Recall={row['Recall']:.4f}"
                f"  Specificity={row['Specificity']:.4f}{tag}"
            )

        logger.info("-" * 70)


def main() -> None:
    """Entry point for the pipeline (used by poetry scripts)."""
    runner = ExperimentRunner()
    runner.run()
