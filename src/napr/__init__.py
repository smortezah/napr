"""Napr package."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("napr")
except PackageNotFoundError:
    __version__ = "unknown"
