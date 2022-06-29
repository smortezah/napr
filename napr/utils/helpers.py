"""Helper functions."""

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def all_but(all: list[str], but: list[str] | None) -> list[str]:
    """Returns all items in 'all' but the items in 'but'.

    Args:
        all: All items.
        but: Items to be excluded.
    """
    if not but:
        return all

    return [item for item in all if item not in but]


def split_train_test(
    data: pd.DataFrame,
    target: str | None = None,
    selected_classes: list[str] | None = None,
    test_size: float | None = None,
    random_state: int | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series] | tuple[
    pd.DataFrame, pd.DataFrame
]:
    """Split the data into train and test sets.

    It currently supports a 1d target.

    Args:
        data: The data to be split.
        target: The target column. Defaults to None.
        selected_classes: The classes of interest in the target. Defaults to
            None.
        test_size: Fraction of the test data. Defaults to None.
        random_state: Random state. Defaults to None.

    Returns:
        The train and test data.
    """
    if target and selected_classes:
        X_train = data[data[target].isin(selected_classes)]
    else:
        X_train = data.copy()

    if not target:
        X_train, X_test = train_test_split(
            X_train, test_size=test_size, random_state=random_state
        )
        return X_train, X_test

    y_train = X_train.pop(target)
    X_train, X_test, y_train, y_test = train_test_split(
        X_train, y_train, test_size=test_size, random_state=random_state
    )
    return X_train, X_test, y_train, y_test


def label_encode(
    train: pd.Series, test: pd.Series
) -> tuple[np.ndarray, np.ndarray, dict[str, int]]:
    """Encode 1d train and test data with labal encoder.

    Args:
        train: The train data.
        test: The test data.

    Returns:
        The encoded train and test data along with the labels, which shows the
            mapping of the original labels to the encoded labels.
    """
    label_encoder = LabelEncoder()
    train_encoded = label_encoder.fit_transform(train.values.ravel())
    test_encoded = label_encoder.transform(test.values.ravel())
    labels = dict(
        zip(
            label_encoder.classes_,
            label_encoder.transform(label_encoder.classes_),
        )
    )
    return train_encoded, test_encoded, labels
