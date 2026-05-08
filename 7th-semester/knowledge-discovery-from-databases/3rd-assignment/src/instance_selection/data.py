"""Dataset loading and MinMax normalisation."""

import logging
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Dataset:
    """Normalised feature matrix and corresponding class labels.

    Attributes:
        X:            2-D float array of shape (n_samples, n_features).
        y:            1-D string array of class labels, length n_samples.
        feature_names: Original feature column names.
        name:         Human-readable dataset identifier.
    """

    X:             np.ndarray
    y:             np.ndarray
    feature_names: list[str]
    name:          str

    def to_dataframe(self) -> pd.DataFrame:
        """Reconstruct a DataFrame with feature columns and a 'class' column."""
        df = pd.DataFrame(self.X, columns=self.feature_names)
        df["class"] = self.y
        return df


class DataLoader:
    """Reads a CSV, separates the class column, and applies MinMax normalisation.

    The class column must be named ``"class"``.  All other columns are treated
    as numeric features and scaled to [0, 1].

    Args:
        decimals: Number of decimal places to round normalised values to.
    """

    def __init__(self, decimals: int = 6) -> None:
        self._decimals = decimals

    def load(self, path: Path, name: str | None = None) -> Dataset:
        """Load and normalise one CSV dataset.

        Args:
            path: Path to the CSV file.
            name: Optional label for logging / output filenames.

        Returns:
            :class:`Dataset` with normalised features and original class labels.
        """
        name = name or path.stem
        logger.info("Loading dataset '%s' from %s", name, path)

        df = pd.read_csv(path)

        if "class" not in df.columns:
            raise ValueError(f"Dataset at {path} has no 'class' column.")

        y             = df["class"].to_numpy(dtype=str)
        feature_cols  = [c for c in df.columns if c != "class"]
        X_raw         = df[feature_cols].to_numpy(dtype=np.float64)

        scaler = MinMaxScaler()
        X_norm = np.around(scaler.fit_transform(X_raw), decimals=self._decimals)

        logger.info(
            "  %d samples, %d features, %d classes",
            len(y), X_norm.shape[1], len(np.unique(y)),
        )
        return Dataset(X=X_norm, y=y, feature_names=feature_cols, name=name)
