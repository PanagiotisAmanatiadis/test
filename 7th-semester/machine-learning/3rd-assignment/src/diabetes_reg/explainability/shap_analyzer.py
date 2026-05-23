"""SHAP explainability: TreeExplainer for tree models, KernelExplainer otherwise."""

from __future__ import annotations

from pathlib import Path
from typing import Any, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from loguru import logger
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor


class SHAPAnalyzer:
    """Generates SHAP summary and waterfall plots for any fitted sklearn regressor.

    Routes to ``shap.TreeExplainer`` for Random Forest and Gradient Boosting
    (exact, fast) and ``shap.KernelExplainer`` for all other models (model-
    agnostic, limited to a background sample for speed).

    Every public method is fully protected by try/except — SHAP failures
    never halt the outer cross-validation loop.
    """

    def __init__(
        self,
        feature_names: List[str],
        figures_dir: str,
        random_state: int,
    ) -> None:
        """Initialize SHAPAnalyzer.

        Args:
            feature_names: List of feature column names for plot labels.
            figures_dir: Root figures directory; SHAP plots go into
                         ``<figures_dir>/shap/``.
            random_state: Integer seed used for KernelExplainer background
                          sampling.
        """
        self._feature_names = feature_names
        self._shap_dir = Path(figures_dir) / "shap"
        self._shap_dir.mkdir(parents=True, exist_ok=True)
        self._random_state = random_state

    def analyze(
        self,
        model: Any,
        X_train: np.ndarray,
        X_test: np.ndarray,
        model_name: str,
        fold: int,
    ) -> None:
        """Run SHAP analysis and save summary + waterfall plots.

        Uses TreeExplainer for Random Forest and Gradient Boosting, and
        KernelExplainer for Gaussian Process and Ridge.  The entire method
        body is wrapped in try/except so that any SHAP error is logged as a
        warning and the pipeline loop continues uninterrupted.

        Args:
            model: Fitted best_estimator_ from RandomizedSearchCV.
            X_train: Normalized training features for this fold (N_train, F).
            X_test: Normalized test features for this fold (N_test, F).
            model_name: Display name used in plot titles and file names.
            fold: Zero-based fold index.
        """
        try:
            logger.info("    Running SHAP for %s (fold %d)...", model_name, fold + 1)

            X_train_df = pd.DataFrame(X_train, columns=self._feature_names)
            X_test_df = pd.DataFrame(X_test, columns=self._feature_names)
            model_safe = model_name.replace(" ", "_")

            tree_types = (RandomForestRegressor, GradientBoostingRegressor)

            if isinstance(model, tree_types):
                self._tree_explainer(model, X_test_df, model_name, model_safe, fold)
            else:
                self._kernel_explainer(
                    model, X_train_df, X_test_df, model_name, model_safe, fold
                )

        except Exception as shap_err:
            logger.warning(
                "    SHAP analysis skipped for %s fold %d: %s",
                model_name,
                fold + 1,
                shap_err,
            )
            logger.warning("    Pipeline continues.")

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _tree_explainer(
        self,
        model: Any,
        X_test_df: pd.DataFrame,
        model_name: str,
        model_safe: str,
        fold: int,
    ) -> None:
        """Run TreeExplainer and save summary + waterfall plots.

        Args:
            model: Fitted tree-based estimator.
            X_test_df: Test features as a labelled DataFrame.
            model_name: Display name for plot titles.
            model_safe: Filesystem-safe version of model_name.
            fold: Zero-based fold index.
        """
        explainer = shap.TreeExplainer(model)
        shap_vals = explainer(X_test_df)

        # Summary plot
        fig = plt.figure(figsize=(10, 7))
        shap.summary_plot(shap_vals, X_test_df, show=False)
        plt.title(
            f"SHAP Summary — {model_name} | Fold {fold + 1}",
            fontsize=11,
            fontweight="bold",
        )
        plt.tight_layout()
        summary_path = self._shap_dir / f"shap_summary_fold{fold + 1}_{model_safe}.png"
        plt.savefig(summary_path, dpi=130, bbox_inches="tight")
        plt.close()
        logger.info("    SHAP summary saved: %s", summary_path)

        # Waterfall plots for 2 distinct test instances
        for inst_idx in range(min(2, len(X_test_df))):
            try:
                fig = plt.figure(figsize=(10, 6))
                shap.plots.waterfall(shap_vals[inst_idx], show=False)
                plt.title(
                    f"SHAP Waterfall — {model_name} | Fold {fold + 1} | Instance {inst_idx}",
                    fontsize=10,
                    fontweight="bold",
                )
                plt.tight_layout()
                wf_path = (
                    self._shap_dir
                    / f"shap_waterfall_fold{fold + 1}_{model_safe}_inst{inst_idx}.png"
                )
                plt.savefig(wf_path, dpi=130, bbox_inches="tight")
                plt.close()
                logger.info(
                    "    SHAP waterfall (inst %d) saved: %s", inst_idx, wf_path
                )
            except Exception as wf_err:
                logger.warning(
                    "    Waterfall plot failed (inst %d): %s", inst_idx, wf_err
                )

    def _kernel_explainer(
        self,
        model: Any,
        X_train_df: pd.DataFrame,
        X_test_df: pd.DataFrame,
        model_name: str,
        model_safe: str,
        fold: int,
    ) -> None:
        """Run KernelExplainer and save summary + waterfall plots.

        Limits background to 50 samples and explanation set to 30 instances
        for acceptable runtime with slow models like Gaussian Process.

        Args:
            model: Fitted estimator (non-tree).
            X_train_df: Training features as a labelled DataFrame.
            X_test_df: Test features as a labelled DataFrame.
            model_name: Display name for plot titles.
            model_safe: Filesystem-safe version of model_name.
            fold: Zero-based fold index.
        """
        background = shap.sample(
            X_train_df,
            min(50, len(X_train_df)),
            random_state=self._random_state,
        )
        explainer = shap.KernelExplainer(model.predict, background)
        X_explain = X_test_df.iloc[:30]
        shap_vals_k = explainer.shap_values(X_explain)

        # Summary plot
        fig = plt.figure(figsize=(10, 7))
        shap.summary_plot(
            shap_vals_k,
            X_explain,
            feature_names=self._feature_names,
            show=False,
        )
        plt.title(
            f"SHAP Summary — {model_name} | Fold {fold + 1}",
            fontsize=11,
            fontweight="bold",
        )
        plt.tight_layout()
        summary_path = self._shap_dir / f"shap_summary_fold{fold + 1}_{model_safe}.png"
        plt.savefig(summary_path, dpi=130, bbox_inches="tight")
        plt.close()
        logger.info("    SHAP summary saved: %s", summary_path)

        # Waterfall plots via shap.Explanation objects
        base_val = explainer.expected_value
        for inst_idx in range(min(2, len(X_explain))):
            try:
                sv = (
                    shap_vals_k[inst_idx]
                    if hasattr(shap_vals_k, "__len__")
                    else shap_vals_k
                )
                expl_obj = shap.Explanation(
                    values=sv,
                    base_values=base_val,
                    data=X_explain.iloc[inst_idx].values,
                    feature_names=self._feature_names,
                )
                fig = plt.figure(figsize=(10, 6))
                shap.plots.waterfall(expl_obj, show=False)
                plt.title(
                    f"SHAP Waterfall — {model_name} | Fold {fold + 1} | Instance {inst_idx}",
                    fontsize=10,
                    fontweight="bold",
                )
                plt.tight_layout()
                wf_path = (
                    self._shap_dir
                    / f"shap_waterfall_fold{fold + 1}_{model_safe}_inst{inst_idx}.png"
                )
                plt.savefig(wf_path, dpi=130, bbox_inches="tight")
                plt.close()
                logger.info(
                    "    SHAP waterfall (inst %d) saved: %s", inst_idx, wf_path
                )
            except Exception as wf_err:
                logger.warning(
                    "    Waterfall plot failed (inst %d): %s", inst_idx, wf_err
                )
