# Assignment 2 - Fashion-MNIST: Dimensionality Reduction & Clustering Pipeline

**University of Macedonia | Applied Informatics | Machine Learning | 7th Semester 2022–2023**

## Overview

This project evaluates combinations of 5 dimensionality reduction techniques and 5 clustering algorithms on the Fashion-MNIST dataset, using 4 evaluation metrics. The pipeline runs twice: once on raw pixel features and once on reduced features.

### Dimensionality Reduction Techniques
1. **PCA** (50 components)
2. **Stacked Autoencoder** (32-dim latent space)
3. **Convolutional SAE** (32-dim latent space)
4. **UMAP** (32 dimensions)
5. **t-SNE** (2 dimensions)

### Clustering Algorithms
1. MiniBatch K-Means (k=10)
2. DBSCAN (eps=0.5)
3. Agglomerative Clustering (Ward linkage, k=10)
4. Gaussian Mixture Model (10 components)
5. HDBSCAN (min_cluster_size=50)

### Evaluation Metrics
1. Calinski-Harabasz Index
2. Davies-Bouldin Index
3. Silhouette Score
4. Adjusted Rand Index

## Setup

```bash
# Install dependencies
poetry install

# Run the full pipeline
poetry run python scripts/run_pipeline.py

# Run with a custom config
poetry run python scripts/run_pipeline.py --config configs/config.yaml

# Run tests
poetry run pytest tests/ -v
```

## Project Structure

```
├── configs/config.yaml           # All hyperparameters
├── data/                         # Downloaded at runtime
├── logs/                         # Pipeline logs (loguru)
├── reports/
│   ├── figures/                  # All generated plots (PNG)
│   ├── results.csv               # Metrics DataFrame
│   └── latex/report.tex          # LaTeX report
├── scripts/run_pipeline.py       # CLI entry point
├── src/fashion_clustering/       # Main package
│   ├── data/dataset.py           # FashionMNISTDataset
│   ├── reduction/                # PCA, SAE, CNN-SAE, UMAP, t-SNE
│   ├── clustering/               # KMeans, DBSCAN, Agglo, GMM, HDBSCAN
│   ├── evaluation/metrics.py     # MetricsEvaluator
│   ├── visualization/plotter.py  # All plot generation
│   ├── pipeline/experiment.py    # ExperimentRunner orchestrator
│   └── utils/                    # Logger, Timer
└── tests/                        # pytest test suite
```

## Output Files

After running the pipeline, the following files are generated:

- `reports/results.csv` — Full results DataFrame with all metrics
- `reports/figures/sample_images.png` — Sample images per class
- `reports/figures/pca_variance_explained.png` — PCA cumulative variance
- `reports/figures/reconstructions_*.png` — Original vs reconstructed images
- `reports/figures/latent_scatter_*.png` — 2D latent space visualizations
- `reports/figures/cluster_results_*.png` — Cluster assignments for selected classes
- `reports/figures/metrics_heatmap.png` — Metrics heatmap
- `reports/figures/metrics_bar_*.png` — Bar charts per metric
- `logs/pipeline_*.log` — Detailed pipeline logs


*University of Macedonia — Machine Learning Assignment 2 | Academic Year 2022–2023*