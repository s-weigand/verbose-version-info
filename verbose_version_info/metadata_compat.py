"""Compatibility module for importlib.metadata in python < 3.8 ."""
try:
    from importlib.metadata import distribution
except ImportError:
    from importlib_metadata import distribution  # type: ignore
