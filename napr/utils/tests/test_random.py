"""Test the random module."""

from napr.utils.random import rand_list_string

import pytest
from contextlib import nullcontext as not_raises


@pytest.mark.parametrize(
    "letters, len_str, size, exception",
    [
        (123, 1, 1, pytest.raises(TypeError)),
        ("", 2, 2, pytest.raises(ValueError)),
        ("abc", 0, 3, pytest.raises(ValueError)),
        ("abc", 2, 0, pytest.raises(ValueError)),
        ("abc", 1, 1, not_raises()),
        ("abc", 3, 2, not_raises()),
    ],
)
def test_rand_list_string(letters, len_str, size, exception):
    """Test the rand_list_string function."""
    with exception:
        rand_list = rand_list_string(letters, len_str, size)
        assert len(rand_list) == size
        for item in rand_list:
            assert len(item) == len_str
