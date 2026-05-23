"""Visualization utilities for the diabetes regression pipeline."""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")  # Must be set before any pyplot import — required for headless

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from loguru import logger
from pathlib import Path


class Plotter:
    """Generates and saves all figures for the diabetes regression pipeline.

    Handles the target distribution histogram and per-fold actual-vs-predicted
    scatter plots.  All figures are saved to disk immediately after creation
    and the matplotlib figure is closed to keep memory usage low.
    """

    def __init__(self, figures_dir: str, dpi: int = 130) -> None:
        """Initialize Plotter.

        Args:
            figures_dir: Root figures directory.  Sub-directories are created
                         automatically on first use.
            dpi: Dots-per-inch for all saved figures.
        """
        self._figures_dir = Path(figures_dir)
        self._dpi = dpi
        self._figures_dir.mkdir(parents=True, exist_ok=True)
        (self._figures_dir / "actual_vs_pred").mkdir(parents=True, exist_ok=True)

    def plot_target_histogram(self, y_series: pd.Series) -> None:
        """Plot and save a frequency histogram for the target column.

        Args:
            y_series: Pandas Series of raw (unscaled) target values in mg/dL.
        """
        logger.info("Generating target histogram...")

        fig, ax = plt.subplots(figsize=(9, 5))
        ax.hist(
            y_series,
            bins=30,
            color="mediumseagreen",
            edgecolor="black",
            alpha=0.85,
        )
        ax.set_xlabel(
            "Diabetes Progression — blood glucose after 1 year (mg/dL)", fontsize=11
        )
        ax.set_ylabel("Frequency", fontsize=11)
        ax.set_title(
            "Distribution of the Diabetes Progression Target Variable",
            fontsize=13,
            fontweight="bold",
        )
        ax.grid(axis="y", linestyle="--", alpha=0.5)

        plt.tight_layout()
        save_path = self._figures_dir / "target_histogram.png"
        plt.savefig(save_path, dpi=self._dpi)
        plt.close()
        logger.info("Target histogram saved: %s", save_path)

    def plot_actual_vs_predicted(
        self,
        y_true_orig: np.ndarray,
        y_pred_orig: np.ndarray,
        model_name: str,
        fold: int,
        split: str,
    ) -> None:
        """Generate and save an actual-vs-predicted scatter plot with ideal line.

        Args:
            y_true_orig: Actual target values in original mg/dL scale.
            y_pred_orig: Predicted target values in original mg/dL scale.
            model_name: Display name of the regression model.
            fold: Zero-based fold index.
            split: Dataset split label, "Train" or "Test".
        """
        fig, ax = plt.subplots(figsize=(7, 6))

        ax.scatter(
            y_true_orig,
            y_pred_orig,
            alpha=0.55,
            color="royalblue",
            edgecolors="white",
            linewidths=0.4,
            s=40,
            label="Predictions",
        )

        # Ideal y = x reference line
        lo = float(min(y_true_orig.min(), y_pred_orig.min()))
        hi = float(max(y_true_orig.max(), y_pred_orig.max()))
        ax.plot([lo, hi], [lo, hi], "r--", linewidth=2, label="Ideal (y = x)")

        ax.set_xlabel("Actual Output (mg/dL)", fontsize=11)
        ax.set_ylabel("Predicted Output (mg/dL)", fontsize=11)
        ax.set_title(
            f"{model_name} — Fold {fold + 1} | {split} set",
            fontsize=12,
            fontweight="bold",
        )
        ax.legend(fontsize=10)
        ax.grid(linestyle="--", alpha=0.4)

        plt.tight_layout()
        model_safe = model_name.replace(" ", "_")
        fname = f"actual_vs_pred_fold{fold + 1}_{split.lower()}_{model_safe}.png"
        save_path = self._figures_dir / "actual_vs_pred" / fname
        plt.savefig(save_path, dpi=self._dpi)
        plt.close()
        logger.debug("Actual vs predicted saved: %s", save_path)
