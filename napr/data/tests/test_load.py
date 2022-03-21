"""Test the data loading functions."""

import pytest

from napr.data._load import load_terpene


def test_load_terpene():
    """Test loading the terpene dataset."""
    # Supported version is 21.3
    with pytest.raises(ValueError):
        load_terpene(download=False, version="20")
