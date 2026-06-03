"""Test the data related functions."""

import pytest

from napr.coconut.data import load_terpene
from napr.network import download


def test_download():
    """Test the download function."""
    with pytest.raises(ValueError):
        download(url="")


@pytest.mark.parametrize(
    "download, path, version, exception",
    [
        (False, ".", "20", pytest.raises(ValueError)),
        (False, "not_a_path", "21.3", pytest.raises(FileNotFoundError)),
    ],
)
def test_load_terpene(download, path, version, exception):
    """Test loading the terpene dataset."""
    with exception:
        load_terpene(download=download, path=path, version=version)
