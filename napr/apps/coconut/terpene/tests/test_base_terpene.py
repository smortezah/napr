"""Test the base class for the terpene app."""

import random
import pandas as pd

import pytest

from napr.apps.coconut.terpene._base import Terpene


@pytest.fixture(scope="module")
def data():
    """Create a test pandas DataFrame."""

    def gen_rand(N=10):
        return [random.random() for _ in range(N)]

    return pd.DataFrame(
        {
            "a": gen_rand(),
            "b": gen_rand(),
            "c": gen_rand(),
        }
    )


def test_base_class(data):
    """Test the Terpene class."""
    terpene = Terpene(data=data)

    assert hasattr(terpene, "data")

    assert isinstance(terpene.data, pd.DataFrame)
    assert terpene.data.shape == (10, 3)
