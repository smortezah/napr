"""Helper functions."""


def all_but(all: list[str], but: list[str] | None) -> list[str]:
    """All items in 'all' but the items in 'but'.

    Args:
        all: All items.
        but: Items to be excluded.

    Returns:
        All items in 'all' but the items in 'but'.
    """
    if not but:
        return all

    return [item for item in all if item not in but]
