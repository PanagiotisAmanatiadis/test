"""Diabetes dataset loading, validation, and normalization."""

from __future__ import annotations

from typing import List, Optional

import numpy as np
import pandas as pd
from loguru import logger
from sklearn.datasets import load_diabetes
from sklearn.preprocessing import MinMaxScaler


class DiabetesDataset:
    """Loads and preprocesses the scikit-learn Diabetes dataset.

    Applies independent Min-Max normalization to features (X) and target (y)
    so that predictions can be accurately denormalized for metric computation.

    Attributes:
        _cfg: OmegaConf configuration object.
        _df: Raw DataFrame containing features + target column.
        _X: Normalized feature matrix of shape (N, 10), values in [0, 1].
        _y: Normalized target vector of shape (N,), values in [0, 1].
        _feature_names: List of the 10 feature column names.
        _scaler_X: Fitted MinMaxScaler for features.
        _scaler_y: Fitted MinMaxScaler for the target.
    """

    def __init__(self, cfg: object) -> None:
        """Initialize DiabetesDataset from an OmegaConf config.

        Args:
            cfg: OmegaConf DictConfig containing at minimum a 'seed' key.
        """
        self._cfg = cfg
        self._df: Optional[pd.DataFrame] = None
        self._X: Optional[np.ndarray] = None
        self._y: Optional[np.ndarray] = None
        self._feature_names: List[str] = []
        self._scaler_X: Optional[MinMaxScaler] = None
        self._scaler_y: Optional[MinMaxScaler] = None

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def load(self) -> None:
        """Load the scikit-learn Diabetes dataset (unscaled).

        Uses the exact loading command from the assignment specification:
        ``load_diabetes(as_frame=True, scaled=False)``.

        Also logs the value range for the 'bmi' feature column.
        """
        logger.info("Loading scikit-learn Diabetes dataset (scaled=False)...")

        diabetes_data = load_diabetes(as_frame=True, scaled=False)

        self._df = diabetes_data.frame
        self._feature_names = list(diabetes_data.feature_names)

        logger.info(
            "Dataset loaded — %d samples x %d columns",
            self._df.shape[0],
            self._df.shape[1],
        )
        logger.info("Features: %s", self._feature_names)

        # Print value range for the 'bmi' column (assignment step 2)
        bmi_col = "bmi" if "bmi" in self._df.columns else self._feature_names[0]
        bmi_min = float(self._df[bmi_col].min())
        bmi_max = float(self._df[bmi_col].max())
        logger.info(
            "Value range for column '%s': [%.4f, %.4f]",
            bmi_col,
            bmi_min,
            bmi_max,
        )

    def check_nan(self) -> None:
        """Audit for NaN values and drop affected rows.

        The sklearn Diabetes dataset is clean by design, but this step
        ensures robustness for any modified or extended version.
        """
        assert self._df is not None, "Call load() first."

        total_nans = int(self._df.isnull().sum().sum())
        if total_nans == 0:
            logger.info("No NaN values detected.")
        else:
            logger.warning("Found %d NaN value(s). Removing affected rows...", total_nans)
            before = len(self._df)
            self._df = self._df.dropna().reset_index(drop=True)
            logger.info(
                "Removed %d row(s). Remaining: %d",
                before - len(self._df),
                len(self._df),
            )

    def normalize(self) -> None:
        """Apply Min-Max scaling independently to X and y.

        Two separate MinMaxScaler objects are stored so predictions can
        be accurately denormalized before metric computation.
        """
        assert self._df is not None, "Call load() first."

        logger.info("Applying Min-Max normalization to X and y...")

        X_raw = self._df[self._feature_names].values
        y_raw = self._df["target"].values.reshape(-1, 1)

        self._scaler_X = MinMaxScaler()
        self._scaler_y = MinMaxScaler()

        self._X = self._scaler_X.fit_transform(X_raw)
        self._y = self._scaler_y.fit_transform(y_raw).ravel()

        logger.info("X shape after normalization: %s", self._X.shape)
        logger.info(
            "y range after normalization: [%.4f, %.4f]",
            float(self._y.min()),
            float(self._y.max()),
        )

    def denormalize_y(self, y_norm: np.ndarray) -> np.ndarray:
        """Inverse-transform a normalized target array back to mg/dL scale.

        Args:
            y_norm: Array of normalized target values in [0, 1].

        Returns:
            Array of target values in original mg/dL scale.
        """
        assert self._scaler_y is not None, "Call normalize() first."
        return self._scaler_y.inverse_transform(y_norm.reshape(-1, 1)).ravel()

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def X(self) -> np.ndarray:
        """Normalized feature matrix (N, 10)."""
        assert self._X is not None, "Call normalize() first."
        return self._X

    @property
    def y(self) -> np.ndarray:
        """Normalized target vector (N,)."""
        assert self._y is not None, "Call normalize() first."
        return self._y

    @property
    def feature_names(self) -> List[str]:
        """List of the 10 feature column names."""
        return self._feature_names

    @property
    def scaler_X(self) -> MinMaxScaler:
        """Fitted MinMaxScaler for the feature matrix."""
        assert self._scaler_X is not None, "Call normalize() first."
        return self._scaler_X

    @property
    def scaler_y(self) -> MinMaxScaler:
        """Fitted MinMaxScaler for the target vector."""
        assert self._scaler_y is not None, "Call normalize() first."
        return self._scaler_y

    @property
    def df(self) -> pd.DataFrame:
        """Raw DataFrame containing features and target column."""
        assert self._df is not None, "Call load() first."
        return self._df
