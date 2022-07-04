"""Test the helper functions."""

import numpy as np
import pandas as pd

import pytest

from napr.utils import all_but, split_train_test, label_encode


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


def test_split_train_test():
    """Test the split_train_test function."""
    # Without target and without selected_classes
    X_train, X_test = split_train_test(  # type: ignore
        data=pd.DataFrame(np.random.rand(10, 3), columns=["a", "b", "c"]),
        test_size=0.4,
    )
    assert X_train.shape == (6, 3)
    assert X_test.shape == (4, 3)

    # With target and without selected_classes
    X_train, X_test, y_train, y_test = split_train_test(  # type: ignore
        data=pd.DataFrame(np.random.rand(10, 3), columns=["a", "b", "c"]),
        target="c",
        test_size=0.4,
    )
    assert X_train.shape == (6, 2)
    assert y_train.shape == (6,)
    assert X_test.shape == (4, 2)
    assert y_test.shape == (4,)

    # With target and with selected_classes
    X_train, X_test, y_train, y_test = split_train_test(  # type: ignore
        data=pd.DataFrame(
            {
                "a": np.random.rand(5),
                "b": [2, 0, 1, 1, 2],
                "c": np.random.rand(5),
                "d": np.random.rand(5),
            }
        ),
        target="b",
        selected_classes=[2, 1],
        test_size=0.5,
    )
    assert X_train.shape == (2, 3)
    assert y_train.shape == (2,)
    assert X_test.shape == (2, 3)
    assert y_test.shape == (2,)
    assert y_train.isin([1, 2]).all()
    assert not y_test.isin([0]).any()

    # Different random states
    data = pd.DataFrame(np.random.rand(50, 2))
    test_size = 0.2
    random_state_1 = 12
    random_state_2 = 890
    X_train_1, X_test_1 = split_train_test(  # type: ignore
        data=data,
        test_size=test_size,
        random_state=random_state_1,
    )
    X_train_2, X_test_2 = split_train_test(  # type: ignore
        data=data,
        test_size=test_size,
        random_state=random_state_2,
    )
    assert not np.array_equal(X_train_1, X_train_2)
    assert not np.array_equal(X_test_1, X_test_2)


@pytest.mark.parametrize(
    "train,test,expected_train_encoded,expected_test_encoded,expected_labels",
    [
        (
            pd.Series(["a", "b", "c"]),
            pd.Series(["a", "b"]),
            np.array([0, 1, 2]),
            np.array([0, 1]),
            {"a": 0, "b": 1, "c": 2},
        ),
        (
            pd.Series(["a", "b", "c"]),
            pd.Series(["c", "a", "b"]),
            np.array([0, 1, 2]),
            np.array([2, 0, 1]),
            {"a": 0, "b": 1, "c": 2},
        ),
        (
            pd.Series(["b", "c", "e", "d"]),
            None,
            np.array([0, 1, 3, 2]),
            None,
            {"b": 0, "c": 1, "d": 2, "e": 3},
        ),
    ],
)
def test_label_encode(
    train, test, expected_train_encoded, expected_test_encoded, expected_labels
):
    """Test the label_encode function."""
    train_encoded, test_encoded, labels = label_encode(train, test)
    assert np.array_equal(train_encoded, expected_train_encoded)
    assert np.array_equal(test_encoded, expected_test_encoded)  # type: ignore
    assert labels == expected_labels


def test_label_encode_exception():
    """Test the label_encode function when exception occurs."""
    with pytest.raises(ValueError):
        label_encode(pd.Series(), pd.Series(1))
