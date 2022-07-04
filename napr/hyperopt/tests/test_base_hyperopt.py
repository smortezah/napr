"""Test the base hyperopt related functions."""

from tempfile import TemporaryDirectory

import numpy as np
import pandas as pd

from sklearn.neighbors import KNeighborsClassifier

import pytest

from napr.hyperopt._base import find_best_models


def test_find_best_models():
    """Test the find_best_models function."""
    # Empty X
    with pytest.raises(ValueError):
        find_best_models(X=pd.DataFrame(), y=np.array(3), hypermodel=None)

    # No hypermodel
    with pytest.raises(ValueError):
        find_best_models(X=np.array(1), y=np.array(2), hypermodel=None)

    # Unknown score
    with pytest.raises(ValueError), TemporaryDirectory() as tmpdir:
        find_best_models(
            X=np.random.rand(10, 2),
            y=np.random.randint(0, 2, 10),
            hypermodel=lambda hp: KNeighborsClassifier(hp.Choice("k", [3])),
            score="score",
            project_name=tmpdir,
        )

    # Different scores
    for score in ["accuracy", "precision", "recall", "f1"]:
        with TemporaryDirectory() as tmpdir:
            best_model = find_best_models(
                X=np.random.rand(10, 2),
                y=np.random.randint(0, 2, 10),
                hypermodel=lambda hp: KNeighborsClassifier(
                    hp.Choice(name="n_neighbors", values=[3, 4])
                ),
                score=score,
                max_trials=1,
                cv=2,
                project_name=tmpdir,
            )
            assert isinstance(best_model, KNeighborsClassifier)
            assert best_model.n_neighbors in [3, 4]  # type: ignore
