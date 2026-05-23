"""Convolutional Stacked Autoencoder (CNN-SAE) dimensionality reduction."""

from __future__ import annotations

import numpy as np
from loguru import logger

from .base import AbstractReducer


class CNNSAEReducer(AbstractReducer):
    """Convolutional Stacked Autoencoder reducer.

    Architecture:
        Encoder: Input(28,28,1) -> Conv2D(32) -> MaxPool -> Conv2D(64) -> MaxPool
                 -> Flatten -> Dense(latent_dim)
        Decoder: Dense(7*7*64) -> Reshape -> ConvT(64) -> UpSample
                 -> ConvT(32) -> UpSample -> ConvT(1, sigmoid)
    """

    def __init__(
        self,
        filters: list[int] | None = None,
        latent_dim: int = 32,
        epochs: int = 30,
        batch_size: int = 256,
        learning_rate: float = 0.001,
        seed: int = 42,
    ) -> None:
        """Initialize CNNSAEReducer.

        Args:
            filters: Number of filters per conv layer.
            latent_dim: Size of the bottleneck layer.
            epochs: Number of training epochs.
            batch_size: Training batch size.
            learning_rate: Adam learning rate.
            seed: Random seed.
        """
        self._filters = filters or [32, 64]
        self._latent_dim = latent_dim
        self._epochs = epochs
        self._batch_size = batch_size
        self._learning_rate = learning_rate
        self._seed = seed
        self._encoder_model = None
        self._autoencoder = None
        logger.info(
            f"CNNSAEReducer initialized — filters={self._filters}, "
            f"latent_dim={latent_dim}, epochs={epochs}"
        )

    def _build_model(self) -> None:
        """Build the convolutional autoencoder architecture."""
        import tensorflow as tf
        from tensorflow import keras
        from tensorflow.keras import layers  # type: ignore

        tf.random.set_seed(self._seed)

        # Encoder
        encoder_input = keras.Input(shape=(28, 28, 1), name="encoder_input")
        x = encoder_input
        x = layers.Conv2D(self._filters[0], 3, padding="same", activation="relu")(x)
        x = layers.MaxPooling2D(2)(x)
        x = layers.Conv2D(self._filters[1], 3, padding="same", activation="relu")(x)
        x = layers.MaxPooling2D(2)(x)
        x = layers.Flatten()(x)
        latent = layers.Dense(self._latent_dim, activation="relu", name="latent")(x)

        # Decoder
        x = layers.Dense(7 * 7 * 64, activation="relu")(latent)
        x = layers.Reshape((7, 7, 64))(x)
        x = layers.Conv2DTranspose(self._filters[1], 3, padding="same", activation="relu")(x)
        x = layers.UpSampling2D(2)(x)
        x = layers.Conv2DTranspose(self._filters[0], 3, padding="same", activation="relu")(x)
        x = layers.UpSampling2D(2)(x)
        decoder_output = layers.Conv2DTranspose(1, 3, padding="same", activation="sigmoid")(x)

        self._autoencoder = keras.Model(encoder_input, decoder_output, name="cnn_sae")
        self._autoencoder.compile(
            optimizer=keras.optimizers.Adam(learning_rate=self._learning_rate),
            loss="mse",
        )
        logger.debug(f"CNN-SAE model built — parameters: {self._autoencoder.count_params()}")

    def fit(self, X_train: np.ndarray, X_val: np.ndarray | None = None) -> CNNSAEReducer:
        """Train the CNN autoencoder.

        Args:
            X_train: Training images of shape (N, 28, 28, 1).
            X_val: Validation images of shape (M, 28, 28, 1).

        Returns:
            Self.
        """
        from tensorflow.keras.callbacks import EarlyStopping  # type: ignore

        logger.info(f"Training CNN-SAE on data with shape {X_train.shape}")
        self._build_model()

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
        logger.info(f"CNN-SAE training complete — final loss: {final_loss:.6f}")

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
            X: Images of shape (N, 28, 28, 1).

        Returns:
            Latent codes of shape (N, latent_dim).
        """
        Z = self._encoder_model.predict(X, verbose=0)
        logger.debug(f"CNN-SAE transform: {X.shape} -> {Z.shape}")
        return Z

    def reconstruct(self, X: np.ndarray) -> np.ndarray | None:
        """Reconstruct images through the full autoencoder.

        Args:
            X: Images of shape (N, 28, 28, 1).

        Returns:
            Reconstructed images of shape (N, 28, 28, 1).
        """
        return self._autoencoder.predict(X, verbose=0)

    @property
    def name(self) -> str:
        """Human-readable name."""
        return "CNN-SAE"
