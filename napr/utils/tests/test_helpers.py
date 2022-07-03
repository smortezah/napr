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
    assert X_train.shape[0] == 6
    assert X_test.shape[0] == 4
    assert X_train.shape[1] == X_test.shape[1] == 3

    # With target and without selected_classes
    X_train, X_test, y_train, y_test = split_train_test(  # type: ignore
        data=pd.DataFrame(np.random.rand(10, 3), columns=["a", "b", "c"]),
        target="c",
        test_size=0.4,
    )
    assert X_train.shape[0] == y_train.shape[0] == 6
    assert X_test.shape[0] == y_test.shape[0] == 4
    assert X_train.shape[1] == X_test.shape[1] == 2

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
    assert X_train.shape[0] == y_train.shape[0] == 2
    assert X_test.shape[0] == y_test.shape[0] == 2
    assert X_train.shape[1] == X_test.shape[1] == 3
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


def test_label_encode():
    """Test the label_encode function."""
    pass
