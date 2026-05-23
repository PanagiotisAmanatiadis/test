"""Tests for clustering strategies."""

import numpy as np
import pytest

from fashion_clustering.clustering.factory import ClusteringFactory
from fashion_clustering.clustering.base import AbstractClusterer


@pytest.fixture
def cluster_data() -> np.ndarray:
    """Create small synthetic data for clustering tests."""
    rng = np.random.RandomState(42)
    # Three well-separated blobs
    X = np.vstack([
        rng.randn(50, 10) + [5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        rng.randn(50, 10) + [0, 5, 0, 0, 0, 0, 0, 0, 0, 0],
        rng.randn(50, 10) + [0, 0, 5, 0, 0, 0, 0, 0, 0, 0],
    ]).astype(np.float32)
    return X


class TestMiniBatchKMeans:
    """Tests for MiniBatchKMeansClusterer."""

    def test_factory_creation(self) -> None:
        """MiniBatchKMeans can be created via factory."""
        clusterer = ClusteringFactory.create("minibatch_kmeans", n_clusters=3, batch_size=32)
        assert isinstance(clusterer, AbstractClusterer)
        assert clusterer.name == "MiniBatchKMeans"

    def test_fit_predict(self, cluster_data: np.ndarray) -> None:
        """MiniBatchKMeans returns correct number of labels."""
        clusterer = ClusteringFactory.create("minibatch_kmeans", n_clusters=3, batch_size=32)
        labels = clusterer.fit_predict(cluster_data)
        assert labels.shape == (150,)
        assert clusterer.n_clusters == 3


class TestDBSCAN:
    """Tests for DBSCANClusterer."""

    def test_fit_predict(self, cluster_data: np.ndarray) -> None:
        """DBSCAN returns labels with correct shape."""
        clusterer = ClusteringFactory.create("dbscan", eps=2.0, min_samples=3)
        labels = clusterer.fit_predict(cluster_data)
        assert labels.shape == (150,)
        assert clusterer.n_clusters >= 1


class TestGMM:
    """Tests for GMMClusterer."""

    def test_fit_predict(self, cluster_data: np.ndarray) -> None:
        """GMM returns labels with correct shape."""
        clusterer = ClusteringFactory.create("gmm", n_components=3)
        labels = clusterer.fit_predict(cluster_data)
        assert labels.shape == (150,)


class TestFactoryErrors:
    """Tests for factory error handling."""

    def test_unknown_clusterer(self) -> None:
        """Unknown key should raise ValueError."""
        with pytest.raises(ValueError, match="Unknown clusterer"):
            ClusteringFactory.create("nonexistent")
