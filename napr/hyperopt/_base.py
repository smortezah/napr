"""Hyperparameter optimization."""

import numpy as np
import pandas as pd

from sklearn import metrics
from sklearn.model_selection import StratifiedKFold
from sklearn.utils.class_weight import compute_sample_weight

import keras_tuner as kt

from typing import TypeVar

EstimatorT = TypeVar("EstimatorT")


def find_best_models(
    X: pd.DataFrame | np.ndarray,
    y: pd.Series | np.ndarray,
    hypermodel: EstimatorT,
    max_trials: int = 10,
    score: str = "accuracy",
    cv: int = 5,
    directory: str = ".",
    project_name: str = "tuner",
    overwrite: bool = False,
    random_state: int | None = None,
    num_models: int = 1,
) -> EstimatorT | list[EstimatorT]:
    """Search the hyperparameters space and find the best model(s).

    Args:
        X: Input data.
        y: Target data (1d).
        hypermodel: Hyper model. Defaults to None.
        max_trials: Maximum number of trials. Defaults to 10.
        score: Score to use for hyperparameter optimization. Defaults to
            'accuracy'.
        cv: Number of folds for cross-validation. Defaults to 5.
        directory: Directory to save the tuner. Defaults to '.' (current
            directory).
        project_name: Project name for the tuner. Defaults to 'tuner'.
        overwrite: Whether to overwrite the tuner if it already exists. Defaults
            to False.
        random_state: The random state. Defaults to None.
        num_models: Number of best models found. Defaults to 1.

    Returns:
        The best model or the list of the best models.
    """
    if X.size == 0 or y.size == 0:
        raise ValueError("X and y must not be empty.")
    if hypermodel is None:
        raise ValueError("hypermodel must not be None.")

    match score:
        case "accuracy":
            score = metrics.accuracy_score
        case "precision":
            score = metrics.precision_score
        case "recall":
            score = metrics.recall_score
        case "f1":
            score = metrics.f1_score
        case _:
            raise ValueError(f"Unknown score: {score}")

    oracle = kt.oracles.BayesianOptimizationOracle(
        objective=kt.Objective("score", "max"),
        max_trials=max_trials,
    )
    cv = StratifiedKFold(cv, shuffle=True, random_state=random_state)

    tuner = kt.tuners.SklearnTuner(
        oracle=oracle,
        hypermodel=hypermodel,
        scoring=metrics.make_scorer(score),
        cv=cv,
        directory=directory,
        project_name=project_name,
        overwrite=overwrite,
    )
    sample_weight = compute_sample_weight("balanced", y)
    tuner.search(X=X, y=y, sample_weight=sample_weight)
    best_models = tuner.get_best_models(num_models=num_models)

    return best_models[0] if num_models == 1 else best_models
