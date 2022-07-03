"""Test the evaluation of classification methods."""

import pytest

import numpy as np
import pandas as pd

from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

from napr.evaluation.classification import _scores_row, eval_classification


def test_scores_row():
    """Test the _scores_row function."""
    # Without estimator
    with pytest.raises(ValueError):
        _scores_row(estimator="", time=1)

    # Without time
    with pytest.raises(ValueError):
        _scores_row(estimator="estimator", time=0)

    # Without y_test or pred
    with pytest.raises(ValueError):
        _scores_row(estimator="estimator", time=1, scoring=["accuracy"])

    row = _scores_row(
        estimator="estimator",
        time=1,
        y_test=pd.Series([1, 2, 1, 3]),
        pred=np.array([1, 2, 2, 3]),
        scoring=["accuracy", "precision", "recall", "f1", "conf_mat"],
    )
    assert row["accuracy"] == 0.75
    assert row["precision"] == 0.875
    assert row["recall"] == 0.75
    assert row["f1"] == 0.75
    np.testing.assert_array_equal(
        row["conf_mat"], np.array([[1, 1, 0], [0, 1, 0], [0, 0, 1]])
    )


def test_eval_classification():
    """Test the eval_classification function."""
    # Empty string estimators
    with pytest.raises(ValueError):
        eval_classification(estimators="", X=np.array(1), y=np.array(1))

    # Without estimators
    with pytest.raises(ValueError):
        eval_classification(estimators=None, X=np.array(1), y=np.array(1))

    # Without X
    with pytest.raises(ValueError):
        eval_classification(
            estimators=KNeighborsClassifier(),
            X=None,  # type: ignore
            y=np.array(1),
        )

    # Without y
    with pytest.raises(ValueError):
        eval_classification(
            estimators=KNeighborsClassifier(),
            X=np.array(1),
            y=None,  # type: ignore
        )

    # Data
    X = np.random.rand(10, 3)
    y = np.random.randint(low=0, high=2, size=10)
    params = {
        "estimators": KNeighborsClassifier(),
        "X": X,
        "y": y,
        "random_state": 777,
        "n_jobs": -1,
    }

    # Default scoring
    scores = eval_classification(**params)
    for metric in ["accuracy", "precision", "recall", "f1", "conf_mat"]:
        assert metric in scores

    # Custom scoring: accuracy
    params["scoring"] = "accuracy"
    scores = eval_classification(**params)
    assert "accuracy" in scores and "precision" not in scores

    # With test_data
    params["estimators"] = {"test_estimator": GaussianNB()}
    len_train = int(0.8 * len(X))
    params["X"] = X[:len_train]
    params["y"] = y[:len_train]
    params["test_data"] = (X[len_train:], y[len_train:])
    scores = eval_classification(**params)
    assert "test_estimator" in scores["estimator"]
