"""Test the evaluation of classification methods."""

import numpy as np
import pandas as pd

from sklearn.neighbors import KNeighborsClassifier

import pytest
from contextlib import nullcontext as not_raises

from napr.evaluation.classification import _scores_row, eval_classification


@pytest.mark.parametrize(
    "estimator, time, scoring, y_test, pred, expected,exception",
    [
        ("", 1, [], None, None, None, pytest.raises(ValueError)),
        ("estimator", 0, [], None, None, None, pytest.raises(ValueError)),
        (
            "estimator",
            1,
            ["accuracy"],
            None,
            None,
            None,
            pytest.raises(ValueError),
        ),
        (
            "estimator",
            1,
            ["accuracy", "precision", "recall", "f1", "conf_mat"],
            pd.Series([1, 2, 1, 3]),
            np.array([1, 2, 2, 3]),
            {
                "accuracy": 0.75,
                "precision": 0.875,
                "recall": 0.75,
                "f1": 0.75,
                "conf_mat": np.array([[1, 1, 0], [0, 1, 0], [0, 0, 1]]),
            },
            not_raises(),
        ),
    ],
)
def test_scores_row(
    estimator, time, scoring, y_test, pred, expected, exception
):
    """Test the _scores_row function."""
    with exception:
        row = _scores_row(
            estimator=estimator,
            time=time,
            y_test=y_test,
            pred=pred,
            scoring=scoring,
        )
        for score in ["accuracy", "precision", "recall", "f1"]:
            assert row[score] == expected[score]
        np.testing.assert_array_equal(row["conf_mat"], expected["conf_mat"])


@pytest.mark.parametrize(
    "estimators, X, y, test_data, scoring, exception",
    [
        ("", np.array(1), np.array(1), None, None, pytest.raises(ValueError)),
        (None, np.array(1), np.array(1), None, None, pytest.raises(ValueError)),
        (
            KNeighborsClassifier(),
            None,
            np.array(1),
            None,
            None,
            pytest.raises(ValueError),
        ),
        (
            KNeighborsClassifier(),
            np.array(1),
            None,
            None,
            None,
            pytest.raises(ValueError),
        ),
        (
            KNeighborsClassifier(),
            np.random.rand(150, 2),
            np.random.randint(0, 3, 150),
            None,
            ["accuracy", "precision", "recall", "f1", "conf_mat"],
            not_raises(),
        ),
        (
            {"test_estimator": KNeighborsClassifier()},
            np.random.rand(8, 3),
            np.random.randint(0, 2, 8),
            (np.random.rand(3, 3), np.random.randint(0, 2, 3)),
            "accuracy",
            not_raises(),
        ),
    ],
)
def test_eval_classification(estimators, X, y, test_data, scoring, exception):
    """Test the eval_classification function."""
    with exception:
        scores = eval_classification(
            estimators=estimators,
            X=X,
            y=y,
            test_data=test_data,
            scoring=scoring,
            random_state=777,
            n_jobs=-1,
        )
        if isinstance(estimators, dict):
            assert "test_estimator" in scores["estimator"]

        if scoring == "accuracy":
            assert "accuracy" in scores and "precision" not in scores
        else:
            for s in scoring:
                assert s in scores
