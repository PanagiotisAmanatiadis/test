"""Factory for creating regression models and their hyperparameter grids."""

from __future__ import annotations

from typing import Any, Dict, Tuple

from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, Matern, WhiteKernel
from sklearn.linear_model import Ridge


class RegressorFactory:
    """Factory that creates all four regression estimators with param grids.

    Each returned estimator is paired with its RandomizedSearchCV
    hyperparameter distribution so the pipeline can iterate over models
    without embedding model-specific logic in the orchestrator.
    """

    @staticmethod
    def create_all(cfg: object, random_state: int) -> Dict[str, Tuple[Any, Dict]]:
        """Build all four regression models with their parameter distributions.

        Args:
            cfg: OmegaConf DictConfig; the ``models`` sub-key is read for
                 grid values where needed (currently grids are constructed
                 directly to support kernel objects that cannot be serialized
                 to plain YAML).
            random_state: Integer seed for reproducibility.

        Returns:
            Dictionary mapping model display name to a (estimator, param_grid)
            tuple suitable for use with ``RandomizedSearchCV``.
        """
        return {
            "Random Forest": (
                RandomForestRegressor(random_state=random_state, n_jobs=-1),
                {
                    "n_estimators": [50, 100, 200],
                    "max_depth": [None, 5, 10, 20],
                    "min_samples_split": [2, 5, 10],
                    "min_samples_leaf": [1, 2, 4],
                    "max_features": ["sqrt", "log2", 0.5],
                },
            ),
            "Gaussian Process": (
                GaussianProcessRegressor(
                    random_state=random_state, normalize_y=True
                ),
                {
                    "kernel": [
                        RBF(length_scale=1.0),
                        Matern(nu=1.5),
                        Matern(nu=2.5),
                        RBF(length_scale=1.0) + WhiteKernel(noise_level=0.1),
                    ],
                    "alpha": [1e-6, 1e-3, 1e-2, 0.1],
                    "n_restarts_optimizer": [0, 3, 5],
                },
            ),
            "Gradient Boosting": (
                GradientBoostingRegressor(random_state=random_state),
                {
                    "n_estimators": [50, 100, 200],
                    "learning_rate": [0.01, 0.05, 0.1, 0.2],
                    "max_depth": [2, 3, 5],
                    "subsample": [0.7, 0.8, 1.0],
                    "min_samples_leaf": [1, 2, 5],
                },
            ),
            "Ridge Regression": (
                Ridge(),
                {
                    "alpha": [0.01, 0.1, 1.0, 10.0, 100.0, 500.0],
                    "fit_intercept": [True, False],
                    "solver": ["auto", "svd", "cholesky", "lsqr"],
                },
            ),
        }
