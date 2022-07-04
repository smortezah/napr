"""Test the base hyperopt related functions."""

from tempfile import TemporaryDirectory

import numpy as np
import pandas as pd

from sklearn.neighbors import KNeighborsClassifier

import pytest
from contextlib import nullcontext as not_raises

from napr.hyperopt._base import find_best_models


@pytest.mark.parametrize(
    "X, y, hypermodel, scores, max_trials, cv, exception",
    [
        (
            pd.DataFrame(),
            np.array(3),
            None,
            ["accuracy"],
            1,
            2,
            pytest.raises(ValueError),
        ),
        (
            np.array(1),
            np.array(2),
            None,
            ["accuracy"],
            1,
            2,
            pytest.raises(ValueError),
        ),
        (
            np.random.rand(10, 2),
            np.random.randint(0, 2, 10),
            lambda hp: KNeighborsClassifier(hp.Choice("k", [3])),
            ["score"],
            1,
            2,
            pytest.raises(ValueError),
        ),
        (
            np.random.rand(10, 2),
            np.random.randint(0, 2, 10),
            lambda hp: KNeighborsClassifier(
                hp.Choice(name="n_neighbors", values=[3, 4])
            ),
            ["accuracy", "precision", "recall", "f1"],
            1,
            2,
            not_raises(),
        ),
    ],
)
def test_find_best_models(X, y, hypermodel, scores, max_trials, cv, exception):
    """Test the find_best_models function."""
    with exception, TemporaryDirectory() as tmpdir:
        for score in scores:
            best_model = find_best_models(
                X=X,
                y=y,
                hypermodel=hypermodel,
                score=score,
                max_trials=max_trials,
                cv=cv,
                project_name=tmpdir,
                overwrite=True,
            )
            assert isinstance(best_model, KNeighborsClassifier)
            assert best_model.n_neighbors in [3, 4]  # type: ignore
