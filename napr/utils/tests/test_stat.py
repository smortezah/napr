"""Test the Statistical calculation functions."""
import pandas as pd

import pytest

from napr.utils import percent_within


@pytest.mark.parametrize(
    "data,interval,inclusive,expected",
    [
        ([2, 3, 5, 7.0, 8], (3, 5), "both", 40),
        (pd.Series([2, 3, 5, 8.6]), (3.00001, 8), "left", 25.0),
        ([2], (-1, 1), "right", 0),
        (pd.Series([3.00, 4, 5, 7]), (1e0, 9.2), "neither", 100),
    ],
)
def test_percent_within(data, interval, inclusive, expected):
    """Test the percent_within function."""
    with pytest.raises(ValueError):
        percent_within(data=[], interval=(2, 5))

    assert (
        percent_within(data=data, interval=interval, inclusive=inclusive)
        == expected
    )
