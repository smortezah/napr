"""Test the evaluation of classification methods."""

import numpy as np
import pandas as pd

import pytest

from napr.evaluation.classification import _scores_row, eval_classification


def test_scores_row():
    """Test the _scores_row function."""
    # Test with no estimator.
    with pytest.raises(ValueError):
        _scores_row(estimator="", time=1)

    # Test with no time.
    with pytest.raises(ValueError):
        _scores_row(estimator="estimator", time=0)

    # Test with no y_test or pred.
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
    pass
