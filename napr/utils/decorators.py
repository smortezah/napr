"""Decorators."""

import functools
import time
from datetime import timedelta


def info(_func=None, *, message: str):
    """Decorator to print a message before and after the function is called, and
    also the run time.

    Args:
        _func (optional): Called function. Defaults to None.
        message (str): The message to be printed. Defaults to "".
    """

    def decor(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(message + "...", end="\r")
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            delta = timedelta(seconds=end_time - start_time)
            hours, minutes, seconds = str(delta).split(":")
            seconds = str(round(float(seconds)))
            print(f"{message} finished in {hours}h:{minutes}m:{seconds}s.")
            return result

        return wrapper

    return decor if _func is None else decor(_func)
