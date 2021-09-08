"""Compatibility module for importlib.metadata in python < 3.8 ."""

try:
    from importlib.metadata import Distribution
    from importlib.metadata import PackageNotFoundError
    from importlib.metadata import PackagePath
    from importlib.metadata import distribution as _distribution
except ImportError:
    from importlib_metadata import Distribution  # type: ignore[no-redef]
    from importlib_metadata import PackageNotFoundError  # type: ignore[no-redef]
    from importlib_metadata import PackagePath  # type: ignore[no-redef]
    from importlib_metadata import distribution as _distribution  # type: ignore[no-redef]
