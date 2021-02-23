"""Main module."""
from typing import NamedTuple

from verbose_version_info.utils import distribution


class VerboseVersionInfo(NamedTuple):
    """Information container for verbose version information."""

    release_version: str
    url: str
    commit_id: str
    vcs: str


def release_version(
    distribution_name: str,
) -> str:
    """Retrieve the release version of a distribution.

    Parameters
    ----------
    distribution_name : str
        The name of the distribution package as a string.

    Returns
    -------
    str
        Version string of the distribution
    """
    return distribution(distribution_name).version
