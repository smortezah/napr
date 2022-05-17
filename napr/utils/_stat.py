"""Statistical calculations API."""

from typing import Union

import pandas as pd


def percent_within(
    data: Union[list, pd.Series],
    interval: tuple[float, float],
    inclusive: str = "both",
) -> float:
    """Percentage of data within an interval.

    Args:
        data (list | pandas.Series): The data.
        interval (tuple[float, float]): The interval.
        inclusive (str, optional): Include boundaries: "both", "neither",
            "left", "right". Defaults to "both".

    Returns:
        str: Percentage of data within the interval.
    """
    data = pd.Series(data, dtype=float)

    if data.empty:
        raise ValueError("Data cannot be empty.")

    len_within = data.between(
        min(interval), max(interval), inclusive=inclusive  # type: ignore
    ).sum()
    return 100 * len_within / len(data)
