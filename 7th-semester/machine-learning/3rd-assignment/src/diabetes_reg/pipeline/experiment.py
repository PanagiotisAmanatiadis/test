"""Experiment pipeline orchestrator for the diabetes regression assignment."""

from __future__ import annotations

import warnings
from pathlib import Path
from typing import List

import pandas as pd
from loguru import logger
from omegaconf import OmegaConf
from sklearn.model_selection import KFold, RandomizedSearchCV

from ..data.dataset import DiabetesDataset
from ..evaluation.metrics import MetricsEvaluator, RegressionResult
from ..explainability.shap_analyzer import SHAPAnalyzer
from ..models.factory import RegressorFactory
from ..utils.logger import setup_logger
from ..utils.timer import Timer
from ..visualization.plotter import Plotter

warnings.filterwarnings("ignore")

CSV_HEADER: List[str] = [
    "Model", "Set", "Fold",
    "Max_n", "RMSE_n", "MAE_n", "MAPE_n",
    "Max", "RMSE", "MAE", "MAPE",
]


class ExperimentRunner:
    """Orchestrates the full diabetes regression pipeline.

    Loads configuration from YAML, initializes all components, and
    executes the complete 6-Fold cross-validation loop with
    RandomizedSearchCV hyperparameter tuning, metric collection,
    scatter-plot generation, and SHAP explainability.
    """

    def __init__(self, config_path: str = "configs/config.yaml") -> None:
        """Initialize ExperimentRunner from a YAML config file.

        Args:
            config_path: Path to the OmegaConf YAML configuration file.
        """
        self._cfg = OmegaConf.load(config_path)
        setup_logger(Path(self._cfg.paths.logs_dir))
        logger.info("ExperimentRunner initialized from %s", config_path)

    def run(self) -> pd.DataFrame:
        """Execute the complete diabetes regression pipeline end-to-end.

        Steps:
            1. Load + NaN-check + normalize dataset.
            2. Plot target distribution histogram.
            3. Initialize csv_data with the exact assignment header.
            4. 6-Fold KFold loop x model loop:
               a. RandomizedSearchCV fit.
               b. Predict on train + test splits.
               c. Denormalize → compute metrics on both scales.
               d. Plot actual vs predicted scatter.
               e. Append row to csv_data.
               f. SHAP analysis (protected — never halts the fold loop).
            5. Save csv_data to CSV.
            6. Return results DataFrame and log ranked RMSE summary.

        Returns:
            DataFrame with one row per (model, fold, split) combination,
            columns matching CSV_HEADER.
        """
        cfg = self._cfg
        seed: int = int(cfg.seed)
        n_folds: int = int(cfg.pipeline.n_folds)
        n_iter: int = int(cfg.pipeline.n_iter_search)
        figures_dir: str = str(cfg.paths.figures_dir)
        dpi: int = int(cfg.visualization.dpi)

        logger.info("")
        logger.info("=" * 70)
        logger.info("  DIABETES PROGRESSION REGRESSION PIPELINE")
        logger.info("  University of Macedonia | Machine Learning | Assignment 3")
        logger.info("=" * 70)

        # ------------------------------------------------------------------
        # 1. Dataset
        # ------------------------------------------------------------------
        dataset = DiabetesDataset(cfg)
        dataset.load()
        dataset.check_nan()
        dataset.normalize()

        # ------------------------------------------------------------------
        # 2. Target histogram
        # ------------------------------------------------------------------
        plotter = Plotter(figures_dir=figures_dir, dpi=dpi)
        plotter.plot_target_histogram(dataset.df["target"])

        # ------------------------------------------------------------------
        # 3. Component initialization
        # ------------------------------------------------------------------
        evaluator = MetricsEvaluator()
        shap_analyzer = SHAPAnalyzer(
            feature_names=dataset.feature_names,
            figures_dir=figures_dir,
            random_state=seed,
        )
        models_config = RegressorFactory.create_all(cfg, random_state=seed)

        # csv_data starts with the exact assignment header
        csv_data: List[List] = [CSV_HEADER.copy()]

        kf = KFold(n_splits=n_folds, shuffle=True, random_state=seed)
        X = dataset.X
        y = dataset.y

        # ------------------------------------------------------------------
        # 4. Cross-validation loop
        # ------------------------------------------------------------------
        for fold_idx, (train_idx, test_idx) in enumerate(kf.split(X)):
            logger.info("")
            logger.info("=" * 70)
            logger.info("  FOLD %d / %d", fold_idx + 1, n_folds)
            logger.info("=" * 70)

            X_train = X[train_idx]
            y_train = y[train_idx]
            X_test = X[test_idx]
            y_test = y[test_idx]

            logger.info("  Train size: %d  |  Test size: %d", len(X_train), len(X_test))

            for model_name, (base_estimator, param_grid) in models_config.items():
                logger.info("")
                logger.info("  Model: %s", model_name)

                # a. Hyperparameter search
                try:
                    with Timer() as elapsed:
                        rscv = RandomizedSearchCV(
                            estimator=base_estimator,
                            param_distributions=param_grid,
                            n_iter=n_iter,
                            cv=3,
                            scoring="neg_root_mean_squared_error",
                            random_state=seed,
                            n_jobs=-1,
                            refit=True,
                            error_score="raise",
                        )
                        rscv.fit(X_train, y_train)
                    best_model = rscv.best_estimator_
                    logger.info(
                        "    Fit completed in %.1fs | Best params: %s",
                        elapsed(),
                        rscv.best_params_,
                    )
                except Exception as fit_err:
                    logger.error("    Training FAILED: %s", fit_err)
                    continue

                # b-e. Evaluate on train and test splits
                for split_name, X_eval, y_eval in [
                    ("Train", X_train, y_train),
                    ("Test", X_test, y_test),
                ]:
                    try:
                        y_pred_norm = best_model.predict(X_eval)

                        # c. Compute metrics (denormalization inside evaluator)
                        norm_m, orig_m = evaluator.evaluate(
                            y_eval, y_pred_norm, dataset.scaler_y
                        )

                        logger.info(
                            "    %-5s | RMSE=%.2f  MAE=%.2f  Max=%.2f  MAPE=%.2f%%",
                            split_name,
                            orig_m["RMSE"],
                            orig_m["MAE"],
                            orig_m["Max"],
                            orig_m["MAPE"],
                        )

                        # d. Scatter plot (requires original-scale arrays)
                        y_true_orig = dataset.denormalize_y(y_eval)
                        y_pred_orig = dataset.denormalize_y(y_pred_norm)
                        plotter.plot_actual_vs_predicted(
                            y_true_orig, y_pred_orig, model_name, fold_idx, split_name
                        )

                        # e. Append CSV row
                        result = RegressionResult(
                            model_name=model_name,
                            split=split_name,
                            fold=fold_idx + 1,
                            max_n=norm_m["Max_n"],
                            rmse_n=norm_m["RMSE_n"],
                            mae_n=norm_m["MAE_n"],
                            mape_n=norm_m["MAPE_n"],
                            max=orig_m["Max"],
                            rmse=orig_m["RMSE"],
                            mae=orig_m["MAE"],
                            mape=orig_m["MAPE"],
                        )
                        csv_data.extend(MetricsEvaluator.results_to_csv_rows([result]))

                    except Exception as eval_err:
                        logger.error(
                            "    Evaluation FAILED (%s / %s): %s",
                            model_name,
                            split_name,
                            eval_err,
                        )

                # f. SHAP (protected inside SHAPAnalyzer.analyze)
                shap_analyzer.analyze(best_model, X_train, X_test, model_name, fold_idx)

        logger.info("")
        logger.info(
            "Cross-validation complete. CSV rows (incl. header): %d", len(csv_data)
        )

        # ------------------------------------------------------------------
        # 5. Save results CSV
        # ------------------------------------------------------------------
        results_df = self._save_results(csv_data, n_folds)

        logger.info("")
        logger.info("Pipeline complete.")
        return results_df

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _save_results(self, csv_data: List[List], n_folds: int) -> pd.DataFrame:
        """Persist csv_data to disk and log ranked RMSE summary.

        Args:
            csv_data: List of rows including the header at index 0.
            n_folds: Number of folds, used in the summary log line.

        Returns:
            DataFrame built from csv_data (header row excluded).
        """
        if len(csv_data) <= 1:
            logger.warning("No results to save. Run run() first.")
            return pd.DataFrame(columns=CSV_HEADER)

        results_csv = str(self._cfg.paths.results_csv)
        save_path = Path(results_csv)
        save_path.parent.mkdir(parents=True, exist_ok=True)

        df_results = pd.DataFrame(csv_data[1:], columns=csv_data[0])
        df_results.to_csv(save_path, index=False)
        logger.info("Results saved: %s", save_path)

        # Ranked summary
        test_df = df_results[df_results["Set"] == "Test"]
        if test_df.empty:
            return df_results

        mean_metrics = (
            test_df.groupby("Model")[["RMSE", "MAE", "MAPE"]]
            .mean()
            .sort_values("RMSE")
        )

        logger.info("")
        logger.info("-" * 70)
        logger.info("  MEAN TEST-SET PERFORMANCE ACROSS %d FOLDS", n_folds)
        logger.info("-" * 70)
        for model, row in mean_metrics.iterrows():
            logger.info(
                "  %-25s RMSE=%.2f  MAE=%.2f  MAPE=%.2f%%",
                model,
                row["RMSE"],
                row["MAE"],
                row["MAPE"],
            )
        logger.info("-" * 70)

        return df_results


def main() -> None:
    """Entry point for the pipeline (used by poetry scripts and CLI)."""
    runner = ExperimentRunner()
    runner.run()
