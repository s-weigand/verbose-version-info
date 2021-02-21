"""Module containing code for version control system retrieval."""
import json
import os
import sys
from pathlib import Path
from typing import NamedTuple
from typing import Optional

from verbose_version_info.verbose_version_info import get_distribution


class VcsInfo(NamedTuple):
    """Information container for url or vcs installed packages."""

    url: str
    commit_id: str
    vcs: str


def get_url_vcs_information(distribution_name: str) -> Optional[VcsInfo]:
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


def get_editable_install_basepath(distribution_name: str) -> Optional[Path]:
    """Get the basepath of and as editable installed package.

    This assumes that a file with ``<distribution_name>.egg-link`` exists
    somewhere in the path (which is at least for pip the case).

    Parameters
    ----------
    distribution_name : str
        The name of the distribution package as a string.

    Returns
    -------
    Optional[Path]
        Path to the root of an as editable installed package.
        E.g. ``pip install -e .``
    """
    distribution_name = get_distribution(distribution_name).metadata.get("name")
    for path_item in sys.path:
        egg_link = os.path.join(path_item, f"{distribution_name}.egg-link")
        if os.path.isfile(egg_link):
            with open(egg_link) as f:
                base_path = os.path.join(*f.read().splitlines(keepends=False))
                return Path(base_path).resolve()
    return None
