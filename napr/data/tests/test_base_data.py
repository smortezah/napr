"""Test the base data related functions."""

import pytest

from napr.data._base import download


def test_download():
    """Test the download function."""
    with pytest.raises(SystemExit):
        download(url="")
