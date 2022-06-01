"""Helper functions."""

from typing import Optional


def all_but(all: list[str], but: Optional[list[str]]) -> list[str]:
    """All items in all but the items in but.

    Args:
        all (list[str]): All items.
        but (Optional[list[str]]): Items to be excluded.

    Returns:
        list[str]: All items in all but the items in but.
    """
    if not but:
        return all

    return [item for item in all if item not in but]
