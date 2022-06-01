"""Test the random module."""

from napr.utils.random import (
    rand_list_int,
    rand_list_float,
    rand_list_string,
    rand_list_choices,
)

import pytest


@pytest.mark.parametrize("low,high,size", [(0, 10, 1), (-7, 0, 2), (-5, 5, 3)])
def test_rand_list_int(low, high, size):
    """Test the rand_list_int function."""
    with pytest.raises(ValueError):
        rand_list_int(low=1, high=5, size=0)

    rand_list = rand_list_int(low, high, size)
    assert len(rand_list) == size
    for item in rand_list:
        assert low <= item <= high


@pytest.mark.parametrize(
    "low,high,size", [(0.0, 1.0, 1), (-1, 0, 2), (-10.0, 10, 4)]
)
def test_rand_list_float(low, high, size):
    """Test the rand_list_float function."""
    with pytest.raises(ValueError):
        rand_list_float(low=0, high=1, size=0)

    rand_list = rand_list_float(low, high, size)
    assert len(rand_list) == size
    for item in rand_list:
        assert low <= item <= high


@pytest.mark.parametrize("letters,len_str,size", [("abc", 1, 1), ("abc", 3, 2)])
def test_rand_list_string(letters, len_str, size):
    """Test the rand_list_string function."""
    with pytest.raises(TypeError):
        rand_list_string(letters=123, len_str=1, size=1)

    with pytest.raises(ValueError):
        rand_list_string(letters="", len_str=2, size=2)

    with pytest.raises(ValueError):
        rand_list_string(letters="abc", len_str=0, size=3)

    with pytest.raises(ValueError):
        rand_list_string(letters="abc", len_str=2, size=0)

    rand_list = rand_list_string(letters, len_str, size)
    assert len(rand_list) == size
    for item in rand_list:
        assert len(item) == len_str


@pytest.mark.parametrize(
    "elements,size", [(["a", "b", "c"], 1), (["ab", "bc", "cd"], 3)]
)
def test_rand_list_choices(elements, size):
    """Test the rand_list_choices function."""
    with pytest.raises(TypeError):
        rand_list_choices(elements=123, size=1)

    with pytest.raises(ValueError):
        rand_list_choices(elements=[], size=2)

    with pytest.raises(ValueError):
        rand_list_choices(elements=["a", "b", "c"], size=0)

    rand_list = rand_list_choices(elements, size)
    assert len(rand_list) == size
    for item in rand_list:
        assert item in elements
