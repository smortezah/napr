"""Test the base class of the terpene app."""

import pandas as pd
import pytest

from napr.apps.coconut.terpene._base import Terpene
from napr.apps.coconut.terpene import explore


def test_base_class(data):
    """Test the Terpene class."""
    terpene = Terpene(data=data)

    assert hasattr(terpene, "data")
    assert isinstance(terpene.data, pd.DataFrame)
    assert terpene.data.shape == (85, 7)

    assert hasattr(terpene, "plot")
    assert isinstance(terpene.plot, explore.Plot)


def test_preprocess(data):
    """Test the preprocessing method."""
    terpene = Terpene(data=data)
    # with pytest.raises(ValueError):
    #     terpene.preprocess(
    #         random_state=777,
    #         unknown_value=9999,
    #         dropped_columns=["molecular_weight"],
    #         target_columns=["chemicalClass"],
    #     )

    terpene.preprocess(
        random_state=777,
        unknown_value=9999,
        dropped_columns=["molecular_weight"],
        target_columns=["chemicalSubClass"],
    )
    assert terpene.data.shape == (85, 6)
    assert "chemicalClass" not in terpene.data.columns
