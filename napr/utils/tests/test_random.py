"""Test the random module."""

from napr.utils.random import rand_list_float, rand_list_string

import pytest


@pytest.mark.parametrize("low, high, size", [(0.0, 1.0, 1), (-1, 0, 2)])
def test_rand_list_float(low, high, size):
    """Test the rand_list_float function."""
    with pytest.raises(ValueError):
        rand_list_float(low=0, high=1, size=0)

    rand_list = rand_list_float(low, high, size)
    assert len(rand_list) == size
    for item in rand_list:
        assert low <= item <= high
