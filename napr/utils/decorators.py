"""Decorators."""

import functools
import time
from datetime import timedelta


def log(_func=None, *, message=""):
    """Decorator to print a message before and after the function is called, and
    also the time it takes to run the function.

    Args:
        _func (optional): Called function. Defaults to None.
        message (str, optional): The message to be printed. Defaults to "".
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
            # run_time = f"{delta.hours}:{delta.minutes}:{delta.seconds}"
            print(
                f"{message} done in {hours}h{minutes}m{round(float(seconds))}s."
            )
            return result

        return wrapper

    return decor if _func is None else decor(_func)
