"""Generate random numbers and strings."""

import random
import string


def rand_list_string(
    letters: str = string.ascii_lowercase, len_str: int = 1, size: int = 1
) -> list[str]:
    """Returns a list of random strings.

    Args:
        letters: The letters to use in the random strings. Defaults to
            string.ascii_lowercase.
        len_str: The length of the strings. Defaults to 1.
        size: The size of the list. Defaults to 1.

    Raises:
        TypeError: if letters is not a string.
        ValueError: if letters is empty.
        ValueError: if len_str is less than 1.
        ValueError: if size is less than 1.
    """
    if not isinstance(letters, str):
        raise TypeError("letters must be a string.")
    if not letters:
        raise ValueError("letters must not be empty.")
    if len_str < 1:
        raise ValueError("len_str must be greater than 0.")
    if size < 1:
        raise ValueError("size must be greater than 0.")

    return [
        "".join(random.choices(population=letters, k=len_str))
        for _ in range(size)
    ]
