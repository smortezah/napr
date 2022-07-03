"""Test the random module."""

from napr.utils.random import rand_list_string

import pytest


@pytest.mark.parametrize("letters,len_str,size", [("abc", 1, 1), ("abc", 3, 2)])
def test_rand_list_string(letters, len_str, size):
    """Test the rand_list_string function."""
    # 'letters' is not string
    with pytest.raises(TypeError):
        rand_list_string(letters=123, len_str=1, size=1)  # type: ignore

    # Empty 'letters'
    with pytest.raises(ValueError):
        rand_list_string(letters="", len_str=2, size=2)

    # 'len_str' is less than 1
    with pytest.raises(ValueError):
        rand_list_string(letters="abc", len_str=0, size=3)

    # 'size' is less than 1
    with pytest.raises(ValueError):
        rand_list_string(letters="abc", len_str=2, size=0)

    rand_list = rand_list_string(letters, len_str, size)
    assert len(rand_list) == size
    for item in rand_list:
        assert len(item) == len_str
