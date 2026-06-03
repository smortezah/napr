"""Decorators."""

import functools
import time
from collections.abc import Callable
from datetime import timedelta
from typing import Any


def info(_func: Callable[..., Any] | None = None, *, message: str) -> Callable[..., Any]:
    """Decorator to print a message before and after the function is called, and also the run time.

    Args:
        _func: Called function. Defaults to None.
        message: The message to be printed. Defaults to "".
    """

    def decor(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
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
