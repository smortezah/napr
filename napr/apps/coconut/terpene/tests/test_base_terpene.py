"""Test the base class for the terpene app."""

import random
import pandas as pd

import pytest

from napr.apps.coconut.terpene._base import Terpene


@pytest.fixture(scope='module')
def data():
    """Create a test pandas DataFrame."""
    return pd.DataFrame({
        'a': [random.random() for _ in range(10)],
        'b': [random.random() for _ in range(10)],
        'c': [random.random() for _ in range(10)],
    })


def test_base_class(data):
    """Test the Terpene class."""
    terpene = Terpene(data=data)

    assert hasattr(terpene, 'data')

    assert isinstance(terpene.data, pd.DataFrame)
    assert terpene.data.shape == (10, 3)
