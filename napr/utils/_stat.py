"""Statistical calculations API."""

import pandas as pd


def percent_within(
        data: pd.Series,
        interval: tuple[float, float],
        inclusive: str = 'both') -> float:
    """Percentage of data within an interval.

    Args:
        data (pd.Series): The data.
        interval (tuple[float, float]): The interval.
        inclusive (str, optional): Include boundaries: "both", "neither",
            "left", "right". Defaults to "both".

    Returns:
        str: Percentage of data within the interval.
    """
    len_within = len(
        data[data.between(min(interval), max(interval), inclusive=inclusive)])
    return 100 * len_within / len(data)
