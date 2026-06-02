"""Test the base class of the terpene app."""

import pandas as pd

from sklearn.decomposition import PCA

import pytest

from napr.apps.coconut.terpene._base import Terpene
from napr.apps.coconut.terpene import explore


def test_base_class(data):
    """Test the Terpene class."""
    terpene = Terpene(data=data)

    assert hasattr(terpene, "data")
    assert isinstance(terpene.data, pd.DataFrame)
    assert terpene.data.shape == data.shape

    assert hasattr(terpene, "plot")
    assert isinstance(terpene.plot, explore.Plot)


def test_preprocess(data, dropped_columns):
    """Test the preprocessing method."""
    len_expanded_bcutDescriptor = 6  # bcutDescriptor is a string of 6 numbers
    len_expanded_textTaxa = 4  # textTaxa: plants, marine, bacteria, fungi

    terpene = Terpene(data=data)
    terpene.preprocess(
        random_state=777,
        unknown_value=9999,
        dropped_columns=dropped_columns,
    )

    assert terpene.data.shape == (
        data.shape[0],
        data.shape[1]
        + len_expanded_bcutDescriptor
        + len_expanded_textTaxa
        - len(dropped_columns),
    )
    assert "chemicalClass" not in terpene.data.columns


def test_dim_reduce(data, dropped_columns):
    """Test the dimension reduction method."""
    terpene = Terpene(data=data)
    terpene.preprocess(dropped_columns=dropped_columns)

    with pytest.raises(ValueError):
        terpene.dim_reduce(model="PCA")

    len_target_col = 1
    n_components = 2
    data_reduced = terpene.dim_reduce(
        model=PCA(n_components=n_components), inplace=False
    )
    assert data_reduced.shape == (data.shape[0], n_components + len_target_col)

    n_components = 3
    terpene.dim_reduce(model=PCA(n_components=n_components), inplace=True)
    assert terpene.data.shape == (data.shape[0], n_components + len_target_col)
