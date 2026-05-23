"""Experiment pipeline orchestrator."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger
from omegaconf import OmegaConf

from ..data.dataset import FashionMNISTDataset
from ..reduction.factory import ReductionFactory
from ..clustering.factory import ClusteringFactory
from ..evaluation.metrics import MetricsEvaluator
from ..visualization.plotter import Plotter
from ..utils.timer import Timer
from ..utils.logger import setup_logger


RESULTS_COLUMNS = [
    "reduction_technique",
    "clustering_algorithm",
    "reduction_train_time",
    "clustering_exec_time",
    "n_clusters",
    "calinski_harabasz",
    "davies_bouldin",
    "silhouette",
    "adjusted_rand_index",
    "feature_space",
]


class ExperimentRunner:
    """Orchestrates the full dimensionality reduction + clustering pipeline.

    Runs all combinations of reducers and clusterers on both raw pixel
    features and reduced features, collecting metrics into a DataFrame.
    """

    def __init__(self, config_path: str = "configs/config.yaml") -> None:
        """Initialize ExperimentRunner from a YAML config file.

        Args:
            config_path: Path to the configuration YAML file.
        """
        self._cfg = OmegaConf.load(config_path)
        setup_logger(Path(self._cfg.paths.logs_dir))
        logger.info(f"ExperimentRunner initialized from {config_path}")

    def run(self) -> pd.DataFrame:
        """Execute the full experiment pipeline.

        Steps:
            1. Load & split data
            2. For each feature space (raw, reduced):
               For each reducer: fit, transform, plot justification
               For each clusterer: fit_predict, compute metrics
            3. Save results to CSV
            4. Plot summary charts

        Returns:
            DataFrame with results for all combinations.
        """
        cfg = self._cfg
        seed = cfg.seed

        # 1. Load data
        dataset = FashionMNISTDataset(val_split=cfg.data.val_split, seed=seed)

        # Initialize components
        plotter = Plotter(
            figures_dir=cfg.paths.figures_dir,
            dpi=cfg.visualization.dpi,
            style=cfg.visualization.style,
            palette=cfg.visualization.palette,
        )
        evaluator = MetricsEvaluator(seed=seed)
        selected_classes = list(cfg.visualization.selected_classes)

        # Plot sample images
        plotter.plot_sample_images(dataset.X_test, dataset.y_test, seed=seed)

        results: list[dict] = []

        reducer_keys = list(cfg.reduction.keys())
        clusterer_keys = list(cfg.clustering.keys())

        for feature_space in ["raw", "reduced"]:
            logger.info(f"=== Feature space: {feature_space.upper()} ===")

            for r_key in reducer_keys:
                r_cfg = dict(cfg.reduction[r_key])
                # Only pass seed to reducers that accept it
                if r_key in ("sae", "cnn_sae", "umap", "tsne"):
                    r_cfg["seed"] = seed

                # Create reducer
                reducer = ReductionFactory.create(r_key, **r_cfg)
                reducer_name = reducer.name if feature_space == "reduced" else "Raw"

                if feature_space == "raw":
                    # For raw: skip actual reduction, use flattened pixels
                    Z_test = dataset.X_test
                    reduction_time = 0.0

                    # Still plot justification once per reducer in the raw pass
                    # (no — justification plots belong to the reduced pass)
                else:
                    # Fit reducer
                    is_cnn = r_key == "cnn_sae"
                    X_train_fit = dataset.X_train_2d if is_cnn else dataset.X_train
                    X_val_fit = dataset.X_val_2d if is_cnn else dataset.X_val
                    X_test_input = dataset.X_test_2d if is_cnn else dataset.X_test

                    with Timer() as elapsed:
                        reducer.fit(X_train_fit, X_val_fit)
                    reduction_time = elapsed()
                    logger.info(f"{reducer.name} fit took {reduction_time:.2f}s")

                    # Transform test set
                    Z_test = reducer.transform(X_test_input)

                    # Plot justification
                    self._plot_justification(
                        reducer, r_key, dataset, plotter, X_test_input
                    )

                # Run all clusterers on this feature representation
                for c_key in clusterer_keys:
                    c_cfg = dict(cfg.clustering[c_key])
                    if "seed" not in c_cfg and c_key not in ("dbscan", "agglomerative", "hdbscan"):
                        c_cfg["seed"] = seed

                    clusterer = ClusteringFactory.create(c_key, **c_cfg)

                    with Timer() as elapsed:
                        labels = clusterer.fit_predict(Z_test)
                    clustering_time = elapsed()

                    # Evaluate metrics
                    metrics = evaluator.evaluate(Z_test, labels, dataset.y_test)

                    row = {
                        "reduction_technique": reducer_name,
                        "clustering_algorithm": clusterer.name,
                        "reduction_train_time": reduction_time,
                        "clustering_exec_time": clustering_time,
                        "n_clusters": clusterer.n_clusters,
                        "calinski_harabasz": metrics.calinski_harabasz,
                        "davies_bouldin": metrics.davies_bouldin,
                        "silhouette": metrics.silhouette,
                        "adjusted_rand_index": metrics.adjusted_rand_index,
                        "feature_space": feature_space,
                    }
                    results.append(row)
                    logger.info(
                        f"[{feature_space}] {reducer_name} + {clusterer.name} — "
                        f"ARI={metrics.adjusted_rand_index:.4f}"
                    )

                    # Plot cluster results for selected classes
                    plotter.plot_cluster_results(
                        X_images=dataset.X_test,
                        labels=labels,
                        true_labels=dataset.y_test,
                        reducer_name=reducer_name,
                        clusterer_name=clusterer.name,
                        selected_classes=selected_classes,
                    )

                # In raw pass, only run clusterers once (all reducers produce same raw data)
                if feature_space == "raw":
                    break

        # Build results DataFrame
        results_df = pd.DataFrame(results, columns=RESULTS_COLUMNS)
        csv_path = Path(cfg.paths.results_csv)
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        results_df.to_csv(csv_path, index=False)
        logger.info(f"Results saved to {csv_path}")

        # Summary plots
        plotter.plot_metrics_heatmap(results_df)
        for metric in ["calinski_harabasz", "davies_bouldin", "silhouette", "adjusted_rand_index"]:
            plotter.plot_metrics_bar(results_df, metric)

        logger.info("Pipeline complete!")
        return results_df

    def _plot_justification(
        self,
        reducer: object,
        r_key: str,
        dataset: FashionMNISTDataset,
        plotter: Plotter,
        X_test_input: np.ndarray,
    ) -> None:
        """Generate justification plots for a reducer.

        Args:
            reducer: Fitted reducer instance.
            r_key: Reducer config key.
            dataset: The loaded dataset.
            plotter: Plotter instance.
            X_test_input: Test data in the format expected by the reducer.
        """
        # Reconstructions (if supported)
        X_recon = reducer.reconstruct(X_test_input)  # type: ignore
        if X_recon is not None:
            plotter.plot_reconstructions(
                X_test_input[:10], X_recon[:10], reducer.name  # type: ignore
            )

        # PCA variance explained
        if r_key == "pca":
            plotter.plot_variance_explained(reducer.pca)  # type: ignore

        # Latent scatter (use t-SNE for 2D visualization of high-dim latent spaces)
        Z_test = reducer.transform(X_test_input)  # type: ignore
        if Z_test.shape[1] == 2:
            plotter.plot_latent_scatter(Z_test, dataset.y_test, reducer.name)  # type: ignore
        else:
            # Use t-SNE to create 2D visualization of the latent space
            from sklearn.manifold import TSNE
            logger.info(f"Creating t-SNE 2D projection of {reducer.name} latent space")  # type: ignore
            tsne = TSNE(n_components=2, random_state=42, perplexity=30, init="pca", learning_rate="auto")
            # Use a subset for speed
            n_viz = min(5000, Z_test.shape[0])
            Z_2d = tsne.fit_transform(Z_test[:n_viz])
            plotter.plot_latent_scatter(Z_2d, dataset.y_test[:n_viz], reducer.name)  # type: ignore


def main() -> None:
    """Entry point for the pipeline (used by poetry scripts)."""
    runner = ExperimentRunner()
    runner.run()
