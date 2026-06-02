"""Statistical calculations API."""

import pandas as pd


def percent_within(
    data: list[int | float] | pd.Series,
    interval: tuple[float, float],
    inclusive: str = "both",
) -> float:
    """Returns the percentage of data within an interval.

    Args:
        data: The data.
        interval: The interval.
        inclusive: Include boundaries: "both", "neither", "left", "right".
            Defaults to "both".
    """
    data = pd.Series(data, dtype=float)

    if data.empty:
        raise ValueError("Data cannot be empty.")

    len_within = data.between(
        min(interval), max(interval), inclusive=inclusive  # type: ignore
    ).sum()
    return 100 * len_within / len(data)
