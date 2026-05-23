"""Factory for creating clustering strategies."""

from __future__ import annotations

from .base import AbstractClusterer
from .minibatch_kmeans import MiniBatchKMeansClusterer
from .dbscan_clusterer import DBSCANClusterer
from .agglomerative_clusterer import AgglomerativeClusterer
from .gmm_clusterer import GMMClusterer
from .hdbscan_clusterer import HDBSCANClusterer


class ClusteringFactory:
    """Factory for instantiating clustering strategies.

    Uses a registry mapping string keys to clusterer classes.
    """

    _registry: dict[str, type[AbstractClusterer]] = {
        "minibatch_kmeans": MiniBatchKMeansClusterer,
        "dbscan": DBSCANClusterer,
        "agglomerative": AgglomerativeClusterer,
        "gmm": GMMClusterer,
        "hdbscan": HDBSCANClusterer,
    }

    @classmethod
    def create(cls, key: str, **kwargs: object) -> AbstractClusterer:
        """Create a clusterer instance by key.

        Args:
            key: Clusterer identifier (e.g. "minibatch_kmeans", "dbscan").
            **kwargs: Arguments forwarded to the clusterer constructor.

        Returns:
            An instance of the requested clusterer.

        Raises:
            ValueError: If key is not in the registry.
        """
        if key not in cls._registry:
            raise ValueError(f"Unknown clusterer: {key}. Available: {list(cls._registry)}")
        return cls._registry[key](**kwargs)
