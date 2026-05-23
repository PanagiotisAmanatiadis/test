"""Corporate bankruptcy dataset loading and preprocessing."""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from loguru import logger
from omegaconf import DictConfig
from sklearn.preprocessing import MinMaxScaler


class BankruptcyDataset:
    """Loads and preprocesses the corporate bankruptcy Excel dataset.

    Performs column auto-detection, NaN auditing, and Min-Max normalisation.
    Binary labels are remapped: healthy → 0, bankrupt → 1 (positive class).

    Attributes:
        X: Normalised feature matrix (n_samples, n_features).
        y: Binary label vector — 0 = healthy, 1 = bankrupt.
        feature_names: List of feature column names.
        scaler: Fitted MinMaxScaler instance.
        df_raw: Raw DataFrame after NaN removal.
        status_col: Name of the status column.
        year_col: Name of the year column (may be None).
    """

    HEALTHY_LABEL: int = 1
    BANKRUPT_LABEL: int = 2

    def __init__(self, cfg: DictConfig) -> None:
        """Initialise BankruptcyDataset from an OmegaConf config.

        Args:
            cfg: OmegaConf config node containing cfg.data.path and cfg.seed.
        """
        self._data_path = Path(cfg.data.path)
        self._seed = cfg.seed

        self.df_raw: Optional[pd.DataFrame] = None
        self.X: Optional[np.ndarray] = None
        self.y: Optional[np.ndarray] = None
        self.feature_names: List[str] = []
        self.scaler: Optional[MinMaxScaler] = None
        self.status_col: Optional[str] = None
        self.year_col: Optional[str] = None

    # ------------------------------------------------------------------
    def load(self) -> pd.DataFrame:
        """Load the Excel dataset from disk.

        Returns:
            Raw DataFrame.

        Raises:
            FileNotFoundError: If the xlsx file does not exist.
        """
        if not self._data_path.exists():
            raise FileNotFoundError(f"Dataset not found: {self._data_path}")

        logger.info(f"Loading dataset: {self._data_path}")
        self.df_raw = pd.read_excel(self._data_path)
        logger.info(f"Loaded {self.df_raw.shape[0]} rows × {self.df_raw.shape[1]} columns")
        return self.df_raw

    # ------------------------------------------------------------------
    def check_missing_values(self) -> None:
        """Audit for NaN values and drop rows that contain them."""
        assert self.df_raw is not None, "Call load() first."

        nan_total = int(self.df_raw.isnull().sum().sum())
        if nan_total == 0:
            logger.info("No missing values detected.")
            return

        logger.warning(f"Missing values detected — total NaN count: {nan_total}")
        for col, cnt in self.df_raw.isnull().sum()[self.df_raw.isnull().sum() > 0].items():
            logger.warning(f"  Column '{col}': {cnt} NaN(s)")

        before = len(self.df_raw)
        self.df_raw = self.df_raw.dropna().reset_index(drop=True)
        logger.info(f"Dropped {before - len(self.df_raw)} row(s). Remaining: {len(self.df_raw)}")

    # ------------------------------------------------------------------
    def _identify_columns(self) -> Tuple[List[str], str, Optional[str]]:
        """Auto-detect feature, status, and year columns.

        Heuristics:
            Status column : contains exactly the values {1, 2}.
            Year column   : integer values in 1900–2100 with ≤ 50 unique entries.
            Feature cols  : all remaining columns.

        Returns:
            Tuple of (feature_columns, status_column, year_column).
        """
        cols = list(self.df_raw.columns)

        # Detect status column
        status_col: Optional[str] = None
        for c in cols:
            uniq = set(self.df_raw[c].dropna().unique())
            if uniq in ({1, 2}, {1.0, 2.0}):
                status_col = c
                break
        if status_col is None:
            for c in cols:
                if any(kw in c.lower() for kw in ("status", "class", "label", "target")):
                    status_col = c
                    break
        if status_col is None:
            status_col = cols[-2]
            logger.warning(f"Status column not auto-detected; using '{status_col}'")

        # Detect year column
        year_col: Optional[str] = None
        for c in cols:
            if c == status_col:
                continue
            try:
                vals = self.df_raw[c].dropna()
                if vals.between(1900, 2100).all() and vals.nunique() <= 50:
                    year_col = c
                    break
            except TypeError:
                pass
        if year_col is None:
            for c in cols:
                if "year" in c.lower() or "etos" in c.lower():
                    year_col = c
                    break

        exclude = {c for c in [status_col, year_col] if c is not None}
        feature_cols = [c for c in cols if c not in exclude]

        logger.info(f"Status column : '{status_col}'")
        logger.info(f"Year column   : '{year_col}'")
        logger.info(f"Feature cols  : {feature_cols} ({len(feature_cols)} total)")
        return feature_cols, status_col, year_col

    # ------------------------------------------------------------------
    def normalize(self) -> None:
        """Apply Min-Max normalisation to features and remap class labels.

        After calling this method, self.X contains normalised features and
        self.y contains binary labels (0 = healthy, 1 = bankrupt).
        """
        assert self.df_raw is not None, "Call load() first."

        feature_cols, status_col, year_col = self._identify_columns()
        self.status_col = status_col
        self.year_col = year_col

        df = self.df_raw.copy()
        self.scaler = MinMaxScaler()
        df[feature_cols] = self.scaler.fit_transform(df[feature_cols])

        self.X = df[feature_cols].values
        self.y = np.where(df[status_col].values == self.BANKRUPT_LABEL, 1, 0)
        self.feature_names = feature_cols

        n_healthy = int((self.y == 0).sum())
        n_bankrupt = int((self.y == 1).sum())
        logger.info(
            f"Normalisation complete | X: {self.X.shape} | "
            f"Healthy: {n_healthy} | Bankrupt: {n_bankrupt}"
        )
