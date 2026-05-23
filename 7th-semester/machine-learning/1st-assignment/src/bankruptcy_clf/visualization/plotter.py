"""All plot generation for the bankruptcy classification pipeline."""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from loguru import logger


class Plotter:
    """Generates and saves all figures for the classification pipeline.

    Attributes:
        figures_dir: Output directory for PNG files.
        dpi: Figure resolution in dots per inch.
    """

    HEALTHY_LABEL: int = 1
    BANKRUPT_LABEL: int = 2

    def __init__(self, figures_dir: str | Path, dpi: int = 150) -> None:
        """Initialise Plotter.

        Args:
            figures_dir: Directory to save all output figures.
            dpi: DPI for saved figures.
        """
        self.figures_dir = Path(figures_dir)
        self.figures_dir.mkdir(parents=True, exist_ok=True)
        self.dpi = dpi

    # ------------------------------------------------------------------
    def plot_class_distribution_by_year(
        self,
        df: pd.DataFrame,
        status_col: str,
        year_col: str,
    ) -> None:
        """Figure 1: Grouped bar chart of healthy vs bankrupt counts per year.

        Args:
            df: Raw DataFrame containing status and year columns.
            status_col: Name of the company-status column.
            year_col: Name of the fiscal-year column.
        """
        logger.info("Generating Figure 1: class distribution by year …")

        grouped = (
            df.groupby([year_col, status_col])
            .size()
            .unstack(fill_value=0)
            .rename(columns={self.HEALTHY_LABEL: "Healthy", self.BANKRUPT_LABEL: "Bankrupt"})
        )

        x = np.arange(len(grouped))
        width = 0.35

        fig, ax = plt.subplots(figsize=(14, 6))
        bars_h = ax.bar(x - width / 2, grouped.get("Healthy", 0),
                        width, label="Healthy", color="steelblue", alpha=0.85)
        bars_b = ax.bar(x + width / 2, grouped.get("Bankrupt", 0),
                        width, label="Bankrupt", color="crimson", alpha=0.85)

        for bar in (*bars_h, *bars_b):
            h = bar.get_height()
            if h > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, h + 0.5,
                        str(int(h)), ha="center", va="bottom", fontsize=8)

        ax.set_xticks(x)
        ax.set_xticklabels(grouped.index, rotation=45, ha="right")
        ax.set_xlabel("Fiscal Year", fontsize=12)
        ax.set_ylabel("Number of Companies", fontsize=12)
        ax.set_title("Figure 1: Healthy vs Bankrupt Companies per Year",
                     fontsize=14, fontweight="bold")
        ax.legend(fontsize=11)
        ax.grid(axis="y", linestyle="--", alpha=0.5)

        plt.tight_layout()
        path = self.figures_dir / "figure1_class_distribution_by_year.png"
        plt.savefig(path, dpi=self.dpi)
        plt.close()
        logger.info(f"Figure 1 saved: {path}")

    # ------------------------------------------------------------------
    def plot_indicator_statistics(
        self,
        df: pd.DataFrame,
        feature_cols: List[str],
        status_col: str,
    ) -> None:
        """Figure 2: Min/mean/max per indicator for healthy vs bankrupt.

        Args:
            df: Raw DataFrame.
            feature_cols: Names of all feature columns.
            status_col: Name of the status column.
        """
        logger.info("Generating Figure 2: indicator statistics …")

        num_cols = [
            c for c in feature_cols
            if pd.api.types.is_numeric_dtype(df[c]) and df[c].nunique() > 2
        ]
        healthy_df  = df[df[status_col] == self.HEALTHY_LABEL][num_cols]
        bankrupt_df = df[df[status_col] == self.BANKRUPT_LABEL][num_cols]

        def _stats(sub: pd.DataFrame) -> pd.DataFrame:
            return pd.DataFrame({"Min": sub.min(), "Mean": sub.mean(), "Max": sub.max()})

        x, width = np.arange(len(num_cols)), 0.25
        fig, axes = plt.subplots(1, 2, figsize=(18, 7))
        fig.suptitle("Figure 2: Min / Mean / Max per Indicator — Healthy vs Bankrupt",
                     fontsize=14, fontweight="bold")

        panels = [
            (axes[0], _stats(healthy_df),  "Healthy Companies",
             ("royalblue", "steelblue", "navy")),
            (axes[1], _stats(bankrupt_df), "Bankrupt Companies",
             ("salmon", "crimson", "darkred")),
        ]
        for ax, stats, title, colors in panels:
            ax.bar(x - width, stats["Min"],  width, label="Min",  color=colors[0], alpha=0.8)
            ax.bar(x,          stats["Mean"], width, label="Mean", color=colors[1], alpha=0.8)
            ax.bar(x + width,  stats["Max"],  width, label="Max",  color=colors[2], alpha=0.8)
            ax.set_xticks(x)
            ax.set_xticklabels(num_cols, rotation=45, ha="right", fontsize=9)
            ax.set_title(title, fontsize=12, fontweight="bold")
            ax.set_ylabel("Value", fontsize=10)
            ax.legend(fontsize=10)
            ax.grid(axis="y", linestyle="--", alpha=0.4)

        plt.tight_layout()
        path = self.figures_dir / "figure2_indicator_statistics.png"
        plt.savefig(path, dpi=self.dpi)
        plt.close()
        logger.info(f"Figure 2 saved: {path}")

    # ------------------------------------------------------------------
    def plot_confusion_matrix(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        clf_name: str,
        fold: int,
        split: str,
        balanced: bool,
    ) -> None:
        """Save a seaborn confusion matrix heatmap as a PNG.

        Args:
            y_true: Ground-truth labels.
            y_pred: Predicted labels.
            clf_name: Display name of the classifier.
            fold: Zero-based fold index.
            split: "Train" or "Test".
            balanced: True when the training set was undersampled.
        """
        from sklearn.metrics import confusion_matrix as sk_cm

        cm_matrix = sk_cm(y_true, y_pred, labels=[0, 1])
        balance_tag = "Balanced" if balanced else "Unbalanced"

        fig, ax = plt.subplots(figsize=(5, 4))
        sns.heatmap(
            cm_matrix,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=["Healthy", "Bankrupt"],
            yticklabels=["Healthy", "Bankrupt"],
            ax=ax,
        )
        ax.set_title(
            f"{clf_name}\nFold {fold + 1} | {split} | {balance_tag}",
            fontsize=10,
            fontweight="bold",
        )
        ax.set_xlabel("Predicted Label", fontsize=11)
        ax.set_ylabel("True Label", fontsize=11)
        plt.tight_layout()

        clf_safe = clf_name.replace(" ", "_").replace("/", "_")
        fname = f"cm_fold{fold + 1}_{split.lower()}_{clf_safe}_{balance_tag.lower()}.png"
        plt.savefig(self.figures_dir / fname, dpi=self.dpi)
        plt.close()
