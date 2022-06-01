"""Test the preprocessing module."""

import pandas as pd
from napr.utils.random import rand_list_string

import pytest

from napr.apps.coconut.terpene.preprocessing import Preprocess


@pytest.fixture
def preprocessor(data):
    return Preprocess(data=data)


def test_split_bcutDescriptor(preprocessor):
    """Test the _split_bcutDescriptor function."""
    bcutDescriptor = preprocessor.data.pop("bcutDescriptor")
    assert not preprocessor._split_bcutDescriptor()

    preprocessor.data = pd.concat([preprocessor.data, bcutDescriptor], axis=1)
    preprocessor._split_bcutDescriptor()
    for column in ["bcutDescriptor_" + str(i) for i in range(6)]:
        assert column in preprocessor.data.columns


def test_extract_tax(preprocessor):
    """Test the _extract_tax function."""
    textTaxa = preprocessor.data.pop("textTaxa")
    assert not preprocessor._extract_tax()

    preprocessor.data = pd.concat([preprocessor.data, textTaxa], axis=1)
    preprocessor._extract_tax()
    taxes = ["plants", "marine", "bacteria", "fungi"]
    for column in ["textTaxa_" + tax for tax in taxes]:
        assert column in preprocessor.data.columns


def test_encode(preprocessor, train_test_data):
    """Test the _encode function."""
    train_data, test_data = train_test_data
    assert len(train_data) == len(train_test_data[0])
    assert len(test_data) == len(train_test_data[1])

    columns = ['directParentClassification']
    df_columns = train_data[columns]
    train_data.drop(columns, axis=1, inplace=True)
    assert not preprocessor._encode(train_data, test_data)
    train_data = pd.concat([train_data, df_columns], axis=1)

    for col in columns:
        nunique_train = train_data[col].nunique()
        nunique_test = test_data[col].nunique()
        preprocessor._encode(train_data, test_data)
        assert nunique_train == train_data[col].nunique()
        assert nunique_test >= test_data[col].nunique()
