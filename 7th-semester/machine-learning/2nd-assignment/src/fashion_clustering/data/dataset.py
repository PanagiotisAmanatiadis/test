"""Fashion-MNIST dataset loading and preprocessing."""

from __future__ import annotations

import numpy as np
from loguru import logger
from sklearn.model_selection import train_test_split


CLASS_NAMES = [
    "T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
    "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot",
]


class FashionMNISTDataset:
    """Loads and preprocesses the Fashion-MNIST dataset.

    Splits data into train, validation, and test sets with pixel values
    normalized to [0, 1].

    Attributes:
        X_train: Training images flattened to (N, 784), float32 in [0,1].
        X_val: Validation images flattened to (N, 784), float32 in [0,1].
        X_test: Test images flattened to (N, 784), float32 in [0,1].
        y_train: Training labels.
        y_val: Validation labels.
        y_test: Test labels.
        X_train_2d: Training images in (N, 28, 28, 1) for CNN models.
        X_val_2d: Validation images in (N, 28, 28, 1) for CNN models.
        X_test_2d: Test images in (N, 28, 28, 1) for CNN models.
    """

    def __init__(self, val_split: float = 0.1666, seed: int = 42) -> None:
        """Initialize and load the Fashion-MNIST dataset.

        Args:
            val_split: Fraction of training data to use for validation.
            seed: Random seed for reproducibility.
        """
        logger.info("Loading Fashion-MNIST dataset...")
        from tensorflow.keras.datasets import fashion_mnist  # type: ignore

        (X_train_full, y_train_full), (X_test_full, y_test_full) = fashion_mnist.load_data()

        # Normalize to [0, 1]
        X_train_full = X_train_full.astype(np.float32) / 255.0
        X_test_full = X_test_full.astype(np.float32) / 255.0

        # Split train into train + validation
        X_train, X_val, y_train, y_val = train_test_split(
            X_train_full, y_train_full,
            test_size=val_split, random_state=seed, stratify=y_train_full,
        )

        # Store 2D versions for CNN models (N, 28, 28, 1)
        self.X_train_2d = X_train[..., np.newaxis]
        self.X_val_2d = X_val[..., np.newaxis]
        self.X_test_2d = X_test_full[..., np.newaxis]

        # Flatten for non-CNN models (N, 784)
        self.X_train = X_train.reshape(X_train.shape[0], -1)
        self.X_val = X_val.reshape(X_val.shape[0], -1)
        self.X_test = X_test_full.reshape(X_test_full.shape[0], -1)

        self.y_train = y_train
        self.y_val = y_val
        self.y_test = y_test_full

        logger.info(
            f"Dataset loaded — Train: {self.X_train.shape}, "
            f"Val: {self.X_val.shape}, Test: {self.X_test.shape}"
        )
        logger.debug(f"Label distribution (train): {np.bincount(self.y_train)}")
