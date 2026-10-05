"""Module for data container classes."""

from datetime import datetime
from typing import NamedTuple


class VcsInfo(NamedTuple):
    """Container for vcs information."""

    vcs_name: str
    commit_id: str


class VerboseVersionInfo(NamedTuple):
    """Information container for verbose version information."""

    release_version: str
    dist_time: datetime
    url: str = ""
    commit_id: str = ""
    vcs_name: str = ""
