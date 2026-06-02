"""Test the Statistical calculation functions."""

import pandas as pd

import pytest
from contextlib import nullcontext as not_raises

from napr.utils import percent_within


@pytest.mark.parametrize(
    "data, interval, inclusive, expected, exception",
    [
        ([], (2, 5), "both", None, pytest.raises(ValueError)),
        ([2, 3, 5, 7.0, 8], (3, 5), "both", 40, not_raises()),
        (pd.Series([2, 3, 5, 8.6]), (3.00001, 8), "left", 25.0, not_raises()),
        ([2], (-1, 1), "right", 0, not_raises()),
        (pd.Series([3.00, 4, 5, 7]), (1e0, 9.2), "neither", 100, not_raises()),
    ],
)
def test_percent_within(data, interval, inclusive, expected, exception):
    """Test the percent_within function."""
    with exception:
        assert expected == percent_within(
            data=data, interval=interval, inclusive=inclusive
        )
