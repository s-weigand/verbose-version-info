"""Compatibility module for importlib.metadata in python < 3.8 ."""

try:
    from importlib.metadata import Distribution
    from importlib.metadata import PackageNotFoundError
    from importlib.metadata import distribution
except ImportError:
    from importlib_metadata import Distribution  # type: ignore
    from importlib_metadata import PackageNotFoundError  # type: ignore
    from importlib_metadata import distribution  # type: ignore
