"""Stacked Autoencoder (SAE) dimensionality reduction."""

from __future__ import annotations

import numpy as np
from loguru import logger

from .base import AbstractReducer


class SAEReducer(AbstractReducer):
    """Stacked Autoencoder reducer using a fully-connected architecture.

    Architecture:
        Encoder: 784 -> 512 -> 256 -> 128 -> 64 -> latent_dim (ReLU)
        Decoder: latent_dim -> 64 -> 128 -> 256 -> 512 -> 784 (ReLU + Sigmoid)
    """

    def __init__(
        self,
        layers: list[int] | None = None,
        latent_dim: int = 32,
        epochs: int = 30,
        batch_size: int = 256,
        learning_rate: float = 0.001,
        seed: int = 42,
    ) -> None:
        """Initialize SAEReducer.

        Args:
            layers: Encoder hidden layer sizes (excluding latent).
            latent_dim: Size of the bottleneck layer.
            epochs: Number of training epochs.
            batch_size: Training batch size.
            learning_rate: Adam learning rate.
            seed: Random seed.
        """
        self._layers = layers or [512, 256, 128, 64]
        self._latent_dim = latent_dim
        self._epochs = epochs
        self._batch_size = batch_size
        self._learning_rate = learning_rate
        self._seed = seed
        self._encoder_model = None
        self._autoencoder = None
        logger.info(
            f"SAEReducer initialized — layers={self._layers}, "
            f"latent_dim={latent_dim}, epochs={epochs}"
        )

    def _build_model(self, input_dim: int) -> None:
        """Build the autoencoder architecture.

        Args:
            input_dim: Dimensionality of input features.
        """
        import tensorflow as tf
        from tensorflow import keras
        from tensorflow.keras import layers  # type: ignore

        tf.random.set_seed(self._seed)

        # Encoder
        encoder_input = keras.Input(shape=(input_dim,), name="encoder_input")
        x = encoder_input
        for units in self._layers:
            x = layers.Dense(units, activation="relu")(x)
        latent = layers.Dense(self._latent_dim, activation="relu", name="latent")(x)

        # Decoder
        x = latent
        for units in reversed(self._layers):
            x = layers.Dense(units, activation="relu")(x)
        decoder_output = layers.Dense(input_dim, activation="sigmoid", name="decoder_output")(x)

        self._autoencoder = keras.Model(encoder_input, decoder_output, name="sae")
        self._autoencoder.compile(
            optimizer=keras.optimizers.Adam(learning_rate=self._learning_rate),
            loss="mse",
        )
        logger.debug(f"SAE model built — parameters: {self._autoencoder.count_params()}")

    def fit(self, X_train: np.ndarray, X_val: np.ndarray | None = None) -> SAEReducer:
        """Train the stacked autoencoder.

        Args:
            X_train: Training data of shape (N, 784).
            X_val: Validation data of shape (M, 784).

        Returns:
            Self.
        """
        from tensorflow.keras.callbacks import EarlyStopping  # type: ignore

        logger.info(f"Training SAE on data with shape {X_train.shape}")
        self._build_model(X_train.shape[1])

        callbacks = [EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)]
        validation_data = (X_val, X_val) if X_val is not None else None

        history = self._autoencoder.fit(
            X_train, X_train,
            epochs=self._epochs,
            batch_size=self._batch_size,
            validation_data=validation_data,
            callbacks=callbacks,
            verbose=0,
        )
        final_loss = history.history["loss"][-1]
        logger.info(f"SAE training complete — final loss: {final_loss:.6f}")

        # Isolate encoder sub-model
        from tensorflow import keras
        self._encoder_model = keras.Model(
            inputs=self._autoencoder.input,
            outputs=self._autoencoder.get_layer("latent").output,
        )
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Encode data using the trained encoder.

        Args:
            X: Data of shape (N, 784).

        Returns:
            Latent codes of shape (N, latent_dim).
        """
        Z = self._encoder_model.predict(X, verbose=0)
        logger.debug(f"SAE transform: {X.shape} -> {Z.shape}")
        return Z

    def reconstruct(self, X: np.ndarray) -> np.ndarray | None:
        """Reconstruct data through the full autoencoder.

        Args:
            X: Original data of shape (N, 784).

        Returns:
            Reconstructed data of shape (N, 784).
        """
        return self._autoencoder.predict(X, verbose=0)

    @property
    def name(self) -> str:
        """Human-readable name."""
        return "SAE"
