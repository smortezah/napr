"""Generate random numbers and strings."""

import random
import string


def rand_list_int(low: int = 0, high: int = 9, size: int = 1) -> list[int]:
    """Generate a list of random integers.

    Args:
        low (int, optional): The lower bound of the random integers. Defaults to
            0.
        high (int, optional): The upper bound of the random integers. Defaults
            to 9.
        size (int, optional): The size of the list. Defaults to 1.

    Raises:
        ValueError: if size is less than 1.

    Returns:
        list[int]: A list of random integers.
    """
    if size < 1:
        raise ValueError("size must be greater than 0.")

    return [random.randint(low, high) for _ in range(size)]


def rand_list_float(
    low: float = 0.0, high: float = 1.0, size: int = 1
) -> list[float]:
    """Generate a list of random floats.

    Args:
        low (float, optional): The lower bound of the random floats. Defaults to
            0.0.
        high (float, optional): The upper bound of the random floats. Defaults
            to 1.0.
        size (int, optional): The size of the list. Defaults to 1.

    Raises:
        ValueError: if size is less than 1.

    Returns:
        list[float]: A list of random floats.
    """
    if size < 1:
        raise ValueError("size must be greater than 0.")

    return [random.uniform(low, high) for _ in range(size)]


def rand_list_string(
    letters: str = string.ascii_lowercase, len_str: int = 1, size: int = 1
) -> list[str]:
    """Generate a list of random strings.

    Args:
        letters (str, optional): The letters to use in the random strings.
            Defaults to string.ascii_lowercase.
        len_str (int, optional): The length of the strings. Defaults to 1.
        size (int, optional): The size of the list. Defaults to 1.

    Raises:
        TypeError: if letters is not a string.
        ValueError: if letters is empty.
        ValueError: if len_str is less than 1.
        ValueError: if size is less than 1.

    Returns:
        list[str]: A list of random strings
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


def rand_list_choices(elements: list, size: int = 1) -> list:
    """Generate a list of values randomly chosen from a list of elements.

    Args:
        elements (list, optional): The list of elements to choose from. Defaults
            to [].
        size (int, optional): The size of the list. Defaults to 1.

    Raises:
        TypeError: if elements is not a list.
        ValueError: if elements is empty.
        ValueError: if size is less than 1.

    Returns:
        list: A list of values randomly chosen from a list of elements.
    """
    if not isinstance(elements, list):
        raise TypeError("elements must be a list.")
    if not elements:
        raise ValueError("elements must not be empty.")
    if size < 1:
        raise ValueError("size must be greater than 0.")

    return random.choices(population=elements, k=size)
