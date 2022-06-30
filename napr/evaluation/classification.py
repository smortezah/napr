"""Evaluation of the classification methods."""

import time
from tqdm import tqdm

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.utils.class_weight import compute_sample_weight

from typing import Any, TypeVar

EstimatorT = TypeVar("EstimatorT")


def _scores_row(
    estimator: EstimatorT,
    time: float,
    scoring: list[str],
    y_test: pd.Series,
    pred: np.ndarray,
    sample_weight: np.ndarray,
    average: str = "weighted",
    labels: list[str] | None = None,
) -> dict[str, Any]:
    """Reutrns a row of the scores."""
    row = {}
    row["estimator"] = estimator
    row["time"] = time
    if "accuracy" in scoring:
        accuracy = metrics.accuracy_score(
            y_test, pred, sample_weight=sample_weight
        )
        row["accuracy"] = accuracy
    if "precision" in scoring:
        precision = metrics.precision_score(
            y_test,
            pred,
            sample_weight=sample_weight,
            average=average,
        )
        row["precision"] = precision
    if "recall" in scoring:
        recall = metrics.recall_score(
            y_test,
            pred,
            sample_weight=sample_weight,
            average=average,
        )
        row["recall"] = recall
    if "f1" in scoring:
        f1 = metrics.f1_score(
            y_test,
            pred,
            sample_weight=sample_weight,
            average=average,
        )
        row["f1"] = f1
    if "conf_mat" in scoring:
        conf_mat = metrics.confusion_matrix(
            y_test,
            pred,
            sample_weight=sample_weight,
            labels=labels,
            normalize=None,
        )
        row["conf_mat"] = conf_mat
    return row


def eval_classification(
    estimators: dict[str, EstimatorT] | list[EstimatorT],
    X: pd.DataFrame,
    y: pd.Series,
    test_data: tuple[pd.DataFrame, pd.Series] | None = None,
    test_size: float | None = None,
    scoring: list[str] | str | None = None,
    random_state: int | None = None,
    n_jobs: int | None = None,
) -> dict[str, Any]:
    """Evaluate classifiers.

    Args:
        estimators: The classifiers. It is either a list of scikit-learn
            classification models or a dictionary of classifiers with their
            names (string) as keys.
        X: Input data.
        y: The target data (1d).
        test_data: The test/validation data, in the form of (X_test, y_test). If
            not provided, the "test_size" will be considered to split the
            train-test. Defaults to None.
        test_size: Fraction of the test/evaluation data. It defaults to 0.2 in
            case neither of "test_data" nor "test_size" is provided. Defaults to
            None.
        scoring: A score or a list of scores. Defaults to None.
        random_state: Random state. Defaults to None.
        n_jobs: The number of jobs to run in parallel. Defaults to None.

    Returns:
        A dictionary mapping the score names to the evaluation results.
    """
    # Default metrics. If scoring is not specified, the default is used.
    METRICS = ["accuracy", "precision", "recall", "f1", "conf_mat"]

    if not scoring:
        scoring = METRICS
    elif isinstance(scoring, str):
        scoring = [scoring]

    # Either test_data or test_size will be used.
    if test_data:
        test_size = None
    elif not test_data and not test_size:
        test_size = 0.2

    # Names and model objects of the estimators
    if not isinstance(estimators, list) and not isinstance(estimators, dict):
        estimators = [estimators]

    if isinstance(estimators, list):
        estimator_names = [est.__class__.__name__ for est in estimators]
        estimators = {
            name: est for name, est in zip(estimator_names, estimators)
        }

    # Set common attributes for all estimators
    for estimator in estimators.values():
        setattr(estimator, "random_state", random_state)
        setattr(estimator, "n_jobs", n_jobs)

    # Data
    if test_data:
        X_train = X.copy()
        X_test = test_data[0].copy()
        y_train = y.copy()
        y_test = test_data[1].copy()
    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

    # Sample weights
    sample_weight_train = compute_sample_weight("balanced", y_train)
    sample_weight_test = compute_sample_weight("balanced", y_test)

    # Results
    scores = {key: [] for key in ["estimator", "time"] + scoring}

    progress_bar = tqdm(estimators.items())
    for name, estimator in progress_bar:
        progress_bar.set_postfix({"method": name})

        # Training
        start_train = time.perf_counter()
        if estimator.__class__.__name__ == "KNeighborsClassifier":
            estimator.fit(X_train, y_train)
        else:
            estimator.fit(X_train, y_train, sample_weight=sample_weight_train)
        end_train = time.perf_counter()

        # Prediction
        pred = estimator.predict(X_test)

        # Scores
        row = _scores_row(
            estimator=name,
            time=end_train - start_train,
            scoring=scoring,
            y_test=y_test,
            pred=pred,
            sample_weight=sample_weight_test,
            labels=estimator.classes_,
        )
        for key, val in row.items():
            scores[key].append(val)
    progress_bar.close()

    return scores
