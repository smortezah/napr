"""Test the helper functions."""

import pytest

from napr.utils import all_but


@pytest.mark.parametrize(
    "all,but,expected",
    [
        (["a", "b", "c"], ["b", "c"], ["a"]),
        (["a", "b", "c"], ["a", "b", "c"], []),
        (["a", "b", "c"], [], ["a", "b", "c"]),
        ([], ["a", "b", "c"], []),
        ([], [], []),
        (["a", "b", "c"], ["a", "b", "c", "d"], []),
        (["a", "b", "c"], ["d", "e", "f"], ["a", "b", "c"]),
        (["a", "b", "c"], None, ["a", "b", "c"]),
    ],
)
def test_all_but(all, but, expected):
    """Test the all_but function."""
    assert all_but(all=all, but=but) == expected
