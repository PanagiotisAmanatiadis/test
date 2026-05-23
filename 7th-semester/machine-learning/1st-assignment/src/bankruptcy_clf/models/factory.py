"""Factory for instantiating all 8 classifiers."""
from __future__ import annotations

from typing import Any, Dict

from loguru import logger
from omegaconf import DictConfig
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


class ClassifierFactory:
    """Creates all 8 classification models from an OmegaConf config.

    The 8th model is Gradient Boosting Classifier — selected because boosting
    iteratively corrects residuals, making it effective on imbalanced tabular
    financial data.
    """

    @staticmethod
    def create_all(cfg: DictConfig) -> Dict[str, Any]:
        """Instantiate every classifier with parameters from the config.

        Args:
            cfg: OmegaConf config node; uses cfg.classifiers and cfg.seed.

        Returns:
            Ordered dict mapping display name → sklearn estimator.
        """
        seed: int = int(cfg.seed)
        c = cfg.classifiers

        classifiers: Dict[str, Any] = {
            "LDA": LinearDiscriminantAnalysis(),
            "Logistic Regression": LogisticRegression(
                max_iter=int(c.logistic_regression.get("max_iter", 1000)),
                random_state=seed,
            ),
            "Decision Tree": DecisionTreeClassifier(random_state=seed),
            "Random Forest": RandomForestClassifier(
                n_estimators=int(c.random_forest.get("n_estimators", 100)),
                n_jobs=-1,
                random_state=seed,
            ),
            "kNN": KNeighborsClassifier(
                n_neighbors=int(c.knn.get("n_neighbors", 5))
            ),
            "Naive Bayes": GaussianNB(),
            "SVM": SVC(probability=True, random_state=seed),
            "Gradient Boosting": GradientBoostingClassifier(
                n_estimators=int(c.gradient_boosting.get("n_estimators", 100)),
                learning_rate=float(c.gradient_boosting.get("learning_rate", 0.1)),
                random_state=seed,
            ),
        }

        logger.info(f"ClassifierFactory created {len(classifiers)} classifiers.")
        return classifiers
