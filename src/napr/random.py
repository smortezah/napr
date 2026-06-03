"""Generate random numbers and strings."""

import random
import string


def rand_list_string(
    letters: str = string.ascii_lowercase, str_len: int = 1, list_size: int = 1
) -> list[str]:
    """Returns a list of random strings.

    Args:
        letters: The letters to use in the random strings. Defaults to ASCII lowercase letters.
        str_len: The length of the strings. Defaults to 1.
        list_size: The size of the list. Defaults to 1.

    Raises:
        TypeError: if letters is not a string.
        ValueError: if letters is empty.
        ValueError: if str_len is less than 1.
        ValueError: if list_size is less than 1.
    """
    if not isinstance(letters, str):
        raise TypeError("letters must be a string.")
    if not letters:
        raise ValueError("letters must not be empty.")
    if str_len < 1:
        raise ValueError("str_len must be greater than 0.")
    if list_size < 1:
        raise ValueError("list_size must be greater than 0.")

    return ["".join(random.choices(population=letters, k=str_len)) for _ in range(list_size)]
