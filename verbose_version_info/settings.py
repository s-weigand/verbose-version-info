"""Module containing all settings related functionalities."""

from copy import copy

DEFAULT_VCS_SETTINGS = {"warn_dirty": True}
VCS_SETTINGS = copy(DEFAULT_VCS_SETTINGS)

DEFAULT_SETTINGS = {"not_found_version_str": "Unknown", "vcs": VCS_SETTINGS}
SETTINGS = copy(DEFAULT_SETTINGS)
