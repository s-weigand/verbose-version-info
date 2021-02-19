"""Module containing code for version control system retrieval."""
from __future__ import annotations

import json
from typing import NamedTuple

from verbose_version_info.verbose_version_info import get_distribution


class VcsInfo(NamedTuple):
    """Information container for url or vcs installed packages."""

    url: str
    commit_id: str
    vcs: str


def get_url_vcs_information(distribution_name: str) -> VcsInfo | None:
    """Extract package information for packages installed from an url.

    If the packages was installed using an url 'direct_url.json'
    will be parsed and the information extracted.
    If a ``vcs`` (e.g. ``git``) was used, the used ``vcs`` and ``commit_id``
    will be retrieved as well.

    Parameters
    ----------
    distribution_name : str
        The name of the distribution package as a string.

    Examples
    --------
    If the package was installed using git:
    ``pip install git+https://github.com/s-weigand/git-install-test-distribution.git``

    >>> get_url_vcs_information("git-install-test-distribution")
    VcsInfo(
        url="https://github.com/s-weigand/git-install-test-distribution.git",
        commit_id="a7f7bf28dbe9bfceba1af8a259383e398a942ad0",
        vcs="git",
    )

    If the package was installed by an url to a tarball:
    ``pip install https://github.com/s-weigand/git-install-test-distribution/archive/main.zip``

    >>> get_url_vcs_information("git-install-test-distribution")
    VcsInfo(
        url="https://github.com/s-weigand/git-install-test-distribution/archive/main.zip",
        commit_id="",
        vcs="",
    )


    If the package was not installed from an url:
    ``pip install package-name``

    >>> get_url_vcs_information("package-name")
    None

    Returns
    -------
    VcsInfo | None
        VcsInfo
            If the package was installed from a url resource.
        None
            If the package was installed from a local resource or PyPi.
    """
    dist_files = get_distribution(distribution_name).files
    if dist_files is not None:
        for path in dist_files:
            if path.name == "direct_url.json":
                vcs_dict = json.loads(path.read_text())
                url = vcs_dict.get("url", "")
                vcs_info = vcs_dict.get("vcs_info", {})
                commit_id = vcs_info.get("commit_id", "")
                vcs = vcs_info.get("vcs", "")
                return VcsInfo(url, commit_id, vcs)

    return None
