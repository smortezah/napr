"""Test the preprocessing module."""

import pytest

from napr.apps.coconut.terpene.preprocessing import Preprocess


@pytest.fixture
def preprocessor(data):
    return Preprocess(data=data)


def test_split_bcutDescriptor(data, preprocessor):
    """Test the _split_bcutDescriptor function."""
    preprocessor.data.pop("bcutDescriptor")
    assert not preprocessor._split_bcutDescriptor()

    preprocessor.data = data.copy()
    preprocessor._split_bcutDescriptor()
    for column in ["bcutDescriptor_" + str(i) for i in range(6)]:
        assert column in preprocessor.data.columns


def test_extract_tax(preprocessor):
    """Test the _extract_tax function."""
    assert not preprocessor._extract_tax()


# def test_encode():
