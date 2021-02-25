"""Module containing function to look up resources."""

import json
import os
import sys
from pathlib import Path
from typing import List
from typing import Optional
from urllib.parse import unquote
from urllib.parse import urlparse

from verbose_version_info.data_containers import VerboseVersionInfo
from verbose_version_info.utils import distribution


def find_url_info(distribution_name: str) -> Optional[VerboseVersionInfo]:
    """Extract package information for packages installed from an url or locally.

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

    >>> find_url_info("git-install-test-distribution")
    VcsInfo(
        url="https://github.com/s-weigand/git-install-test-distribution.git",
        commit_id="a7f7bf28dbe9bfceba1af8a259383e398a942ad0",
        vcs="git",
    )

    If the package was installed by an url to a tarball:
    ``pip install https://github.com/s-weigand/git-install-test-distribution/archive/main.zip``

    >>> find_url_info("git-install-test-distribution")
    VcsInfo(
        url="https://github.com/s-weigand/git-install-test-distribution/archive/main.zip",
        commit_id="",
        vcs="",
    )


    If the package was not installed from an url or locally:
    ``pip install package-on-pypi``

    >>> find_url_info("package-on-pypi")
    None

    Returns
    -------
    VerboseVersionInfo | None
        VerboseVersionInfo
            If the package was installed from a url resource.
        None
            If the package was installed from as editable or PyPi.
    """
    dist = distribution(distribution_name)
    dist_files = dist.files
    if dist_files is not None:
        for path in dist_files:
            if path.name == "direct_url.json":
                vcs_dict = json.loads(path.read_text())
                vcs_info = vcs_dict.get("vcs_info", {})
                return VerboseVersionInfo(
                    release_version=dist.version,
                    url=vcs_dict.get("url", ""),
                    commit_id=vcs_info.get("commit_id", ""),
                    vcs_name=vcs_info.get("vcs", ""),
                )

    return None


def egg_link_lines(distribution_name: str) -> Optional[List[str]]:
    """Lines of an ``.egg-link`` file if it exists.

    This assumes that a file with ``<distribution_name>.egg-link`` exists
    somewhere in the path (which is at least for pip the case).

    Parameters
    ----------
    distribution_name : str
        The name of the distribution package as a string.

    Returns
    -------
    Optional[List[str]]
        Lines read from ``<distribution_name>.egg-link`` with striped newline.

    See Also
    --------
    find_editable_install_basepath
    """
    distribution_name = distribution(distribution_name).metadata.get("name")
    for path_item in sys.path:
        egg_link = os.path.join(path_item, f"{distribution_name}.egg-link")
        if os.path.isfile(egg_link):
            with open(egg_link) as f:
                return f.read().splitlines(keepends=False)
    return None


def find_editable_install_basepath(distribution_name: str) -> Optional[Path]:
    """Find basepath of an as editable installed package.

    Parameters
    ----------
    distribution_name : str
        The name of the distribution package as a string.

    Returns
    -------
    Optional[Path]
        Path to the root of an as editable installed package.
        E.g. ``pip install -e .``

    See Also
    --------
    egg_link_lines
    """
    egg_link_parts = egg_link_lines(distribution_name)
    if egg_link_parts is not None:
        base_path = os.path.join(*egg_link_parts)
        return Path(base_path).resolve()
    return None


def file_uri_to_path(uri: str) -> Optional[Path]:
    """Convert file uri to a path if the path exists.

    Used to get the base path of local installations from source,
    e.g. ``pip install .`` .

    Parameters
    ----------
    uri : str
        Uri to a file e.g. 'file:///tmp/dist'

    Returns
    -------
    Path
        Path of the file if it exists
    """
    if uri.startswith("file://"):
        parsed_uri = urlparse(uri)
        escape_uri_path = unquote(parsed_uri.path)
        # rare edgecase, thus excluded from coverage
        if sys.platform.startswith("win") and escape_uri_path.startswith("/"):  # pragma: no branch
            escape_uri_path = escape_uri_path[1:]
        path = Path(escape_uri_path)
        if path.exists():
            return path
    return None


def local_install_basepath(
    distribution_name: str, *, vv_info: Optional[VerboseVersionInfo] = None
) -> Optional[Path]:
    """Extract base installation path for packages installed from local resource.

    Parameters
    ----------
    distribution_name : str
        The name of the distribution package as a string.
    vv_info : Optional[VerboseVersionInfo]
        Verbose version info generated by :func:`find_url_info`.

    Returns
    -------
    Optional[Path]
        Path to the root of a package which was installed from a local resource.

    See Also
    --------
    find_url_info
    file_uri_to_path
    find_editable_install_basepath
    """
    if vv_info is None:
        vv_info = find_url_info(distribution_name)
    if vv_info is not None and vv_info.url:
        return file_uri_to_path(vv_info.url)
    else:
        return find_editable_install_basepath(distribution_name)
