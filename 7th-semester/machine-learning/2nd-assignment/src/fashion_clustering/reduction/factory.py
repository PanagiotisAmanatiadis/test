"""Factory for creating dimensionality reduction strategies."""

from __future__ import annotations

from .base import AbstractReducer
from .pca_reducer import PCAReducer
from .sae_reducer import SAEReducer
from .cnn_sae_reducer import CNNSAEReducer
from .umap_reducer import UMAPReducer
from .tsne_reducer import TSNEReducer


class ReductionFactory:
    """Factory for instantiating dimensionality reduction strategies.

    Uses a registry mapping string keys to reducer classes.
    """

    _registry: dict[str, type[AbstractReducer]] = {
        "pca": PCAReducer,
        "sae": SAEReducer,
        "cnn_sae": CNNSAEReducer,
        "umap": UMAPReducer,
        "tsne": TSNEReducer,
    }

    @classmethod
    def create(cls, key: str, **kwargs: object) -> AbstractReducer:
        """Create a reducer instance by key.

        Args:
            key: Reducer identifier (e.g. "pca", "sae").
            **kwargs: Arguments forwarded to the reducer constructor.

        Returns:
            An instance of the requested reducer.

        Raises:
            ValueError: If key is not in the registry.
        """
        if key not in cls._registry:
            raise ValueError(f"Unknown reducer: {key}. Available: {list(cls._registry)}")
        return cls._registry[key](**kwargs)
