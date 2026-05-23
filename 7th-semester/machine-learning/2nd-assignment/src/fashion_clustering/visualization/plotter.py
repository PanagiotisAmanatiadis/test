"""Plotting utilities for the clustering pipeline."""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from loguru import logger

from ..data.dataset import CLASS_NAMES


class Plotter:
    """Generates and saves all required plots for the pipeline.

    All plots are saved to the configured figures directory and
    the figure is closed after saving to free memory.
    """

    def __init__(
        self,
        figures_dir: str = "reports/figures",
        dpi: int = 150,
        style: str = "seaborn-v0_8-whitegrid",
        palette: str = "tab10",
    ) -> None:
        """Initialize Plotter.

        Args:
            figures_dir: Directory to save figures.
            dpi: Resolution for saved figures.
            style: Matplotlib style to use.
            palette: Seaborn color palette.
        """
        self._figures_dir = Path(figures_dir)
        self._figures_dir.mkdir(parents=True, exist_ok=True)
        self._dpi = dpi
        self._style = style
        self._palette = palette
        plt.style.use(style)
        logger.info(f"Plotter initialized — figures_dir={figures_dir}, dpi={dpi}")

    def _save(self, fig: plt.Figure, filename: str) -> None:
        """Save a figure and close it.

        Args:
            fig: Matplotlib figure to save.
            filename: Filename (without directory) to save as.
        """
        path = self._figures_dir / filename
        fig.tight_layout()
        fig.savefig(path, dpi=self._dpi, bbox_inches="tight")
        plt.close(fig)
        logger.info(f"Saved figure: {path}")

    def plot_sample_images(self, X: np.ndarray, y: np.ndarray, seed: int = 42) -> None:
        """Plot one random image per class (10 classes).

        Args:
            X: Flattened images of shape (N, 784).
            y: Labels of shape (N,).
            seed: Random seed for sample selection.
        """
        rng = np.random.RandomState(seed)
        fig, axes = plt.subplots(2, 5, figsize=(12, 5))
        for cls_idx, ax in enumerate(axes.flat):
            indices = np.where(y == cls_idx)[0]
            idx = rng.choice(indices)
            img = X[idx].reshape(28, 28)
            ax.imshow(img, cmap="gray")
            ax.set_title(CLASS_NAMES[cls_idx], fontsize=10)
            ax.axis("off")
        fig.suptitle("Fashion-MNIST Sample Images (one per class)", fontsize=14)
        self._save(fig, "sample_images.png")

    def plot_reconstructions(
        self, X_orig: np.ndarray, X_recon: np.ndarray, reducer_name: str, n: int = 10
    ) -> None:
        """Plot side-by-side original vs reconstructed images.

        Args:
            X_orig: Original images (N, 784) or (N, 28, 28, 1).
            X_recon: Reconstructed images, same shape as X_orig.
            reducer_name: Name of the reducer for the title.
            n: Number of images to display.
        """
        fig, axes = plt.subplots(2, n, figsize=(2 * n, 4))

        for i in range(n):
            orig = X_orig[i]
            recon = X_recon[i]

            if orig.ndim == 1:
                orig = orig.reshape(28, 28)
            elif orig.ndim == 3:
                orig = orig.squeeze()

            if recon.ndim == 1:
                recon = recon.reshape(28, 28)
            elif recon.ndim == 3:
                recon = recon.squeeze()

            axes[0, i].imshow(orig, cmap="gray")
            axes[0, i].axis("off")
            axes[1, i].imshow(recon, cmap="gray")
            axes[1, i].axis("off")

        axes[0, 0].set_ylabel("Original", fontsize=12)
        axes[1, 0].set_ylabel("Reconstructed", fontsize=12)
        fig.suptitle(f"Reconstructions — {reducer_name}", fontsize=14)
        self._save(fig, f"reconstructions_{reducer_name.lower().replace('-', '_')}.png")

    def plot_variance_explained(self, pca_model: object) -> None:
        """Plot cumulative explained variance for PCA.

        Args:
            pca_model: Fitted sklearn PCA instance with explained_variance_ratio_.
        """
        cumvar = np.cumsum(pca_model.explained_variance_ratio_)  # type: ignore
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(range(1, len(cumvar) + 1), cumvar, marker="o", markersize=3)
        ax.set_xlabel("Number of Components")
        ax.set_ylabel("Cumulative Explained Variance")
        ax.set_title("PCA — Cumulative Explained Variance")
        ax.axhline(y=0.95, color="r", linestyle="--", label="95% threshold")
        ax.legend()
        ax.grid(True)
        self._save(fig, "pca_variance_explained.png")

    def plot_latent_scatter(
        self, Z: np.ndarray, y: np.ndarray, reducer_name: str
    ) -> None:
        """Plot 2D scatter of latent representations colored by true label.

        If Z has more than 2 dimensions, only the first two are used.

        Args:
            Z: Latent codes of shape (N, D).
            y: True labels of shape (N,).
            reducer_name: Name of the reducer for the title.
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        palette = sns.color_palette(self._palette, n_colors=10)

        z_plot = Z[:, :2] if Z.shape[1] > 2 else Z

        for cls_idx in range(10):
            mask = y == cls_idx
            ax.scatter(
                z_plot[mask, 0], z_plot[mask, 1],
                c=[palette[cls_idx]], label=CLASS_NAMES[cls_idx],
                s=5, alpha=0.5,
            )
        ax.legend(markerscale=3, fontsize=8)
        ax.set_title(f"Latent Space — {reducer_name}", fontsize=14)
        ax.set_xlabel("Component 1")
        ax.set_ylabel("Component 2")
        self._save(fig, f"latent_scatter_{reducer_name.lower().replace('-', '_')}.png")

    def plot_cluster_results(
        self,
        X_images: np.ndarray,
        labels: np.ndarray,
        true_labels: np.ndarray,
        reducer_name: str,
        clusterer_name: str,
        selected_classes: list[int],
        n_per_cluster: int = 5,
    ) -> None:
        """Plot sample images grouped by predicted cluster for selected classes.

        Args:
            X_images: Flattened images of shape (N, 784).
            labels: Predicted cluster labels of shape (N,).
            true_labels: True class labels of shape (N,).
            reducer_name: Name of the dimensionality reduction technique.
            clusterer_name: Name of the clustering algorithm.
            selected_classes: List of class indices to display.
            n_per_cluster: Number of sample images per cluster.
        """
        unique_clusters = sorted(set(labels))
        if -1 in unique_clusters:
            unique_clusters.remove(-1)

        n_classes = len(selected_classes)
        n_cols = n_per_cluster
        n_rows = n_classes

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(2 * n_cols, 2.5 * n_rows))
        if n_rows == 1:
            axes = axes[np.newaxis, :]

        rng = np.random.RandomState(42)
        for row, cls_idx in enumerate(selected_classes):
            cls_mask = true_labels == cls_idx
            cls_indices = np.where(cls_mask)[0]

            for col in range(n_cols):
                if col < len(cls_indices):
                    idx = rng.choice(cls_indices)
                    img = X_images[idx].reshape(28, 28)
                    cluster_label = labels[idx]
                    axes[row, col].imshow(img, cmap="gray")
                    axes[row, col].set_title(f"C={cluster_label}", fontsize=8)
                axes[row, col].axis("off")

            axes[row, 0].set_ylabel(CLASS_NAMES[cls_idx], fontsize=9, rotation=0, labelpad=50)

        fig.suptitle(
            f"Cluster Results — {reducer_name} + {clusterer_name}", fontsize=13
        )
        fname = (
            f"cluster_results_{reducer_name.lower().replace('-', '_')}_"
            f"{clusterer_name.lower().replace('-', '_')}.png"
        )
        self._save(fig, fname)

    def plot_metrics_heatmap(self, results_df: pd.DataFrame) -> None:
        """Plot a heatmap of all metrics across technique combinations.

        Args:
            results_df: Results DataFrame with columns per the schema.
        """
        metrics = ["calinski_harabasz", "davies_bouldin", "silhouette", "adjusted_rand_index"]
        df = results_df.copy()
        df["combination"] = df["reduction_technique"] + " + " + df["clustering_algorithm"]

        pivot_data = df.set_index("combination")[metrics]

        fig, ax = plt.subplots(figsize=(10, max(6, len(pivot_data) * 0.4)))
        sns.heatmap(
            pivot_data.astype(float), annot=True, fmt=".3f", cmap="YlOrRd",
            ax=ax, linewidths=0.5,
        )
        ax.set_title("Clustering Metrics Heatmap", fontsize=14)
        ax.set_ylabel("")
        self._save(fig, "metrics_heatmap.png")

    def plot_metrics_bar(self, results_df: pd.DataFrame, metric: str) -> None:
        """Plot a bar chart comparing all combinations for a single metric.

        Args:
            results_df: Results DataFrame.
            metric: Column name of the metric to plot.
        """
        df = results_df.copy()
        df["combination"] = df["reduction_technique"] + " + " + df["clustering_algorithm"]

        fig, ax = plt.subplots(figsize=(12, 6))
        colors = sns.color_palette(self._palette, n_colors=len(df))
        bars = ax.barh(df["combination"], df[metric].astype(float), color=colors)
        ax.set_xlabel(metric.replace("_", " ").title())
        ax.set_title(f"Comparison — {metric.replace('_', ' ').title()}", fontsize=14)
        ax.invert_yaxis()
        self._save(fig, f"metrics_bar_{metric}.png")
