"""Statistical calculations API."""

from typing import Literal

import pandas as pd


def percent_within(
    data: list[int | float] | pd.Series,
    interval: tuple[float, float],
    inclusive: Literal["both", "neither", "left", "right"] = "both",
) -> float:
    """Returns the percentage of data within an interval.

    Examples:
        The interval (2, 4) includes 2, 3, and 4, forming 3/5 values, which is 60% of the data.

        >>> percent_within([1, 2, 3, 4, 5], (2, 4))
        60.0
    """
    _data = pd.Series(data, dtype=float)
    if _data.empty:
        raise ValueError("Data cannot be empty.")

    len_within: int = _data.between(
        left=min(interval), right=max(interval), inclusive=inclusive
    ).sum()
    return float(100 * len_within / len(_data))
