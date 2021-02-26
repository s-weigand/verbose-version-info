"""Main module."""

from datetime import datetime

from verbose_version_info.data_containers import VerboseVersionInfo
from verbose_version_info.resource_finders import dist_info_mtime
from verbose_version_info.resource_finders import find_url_info
from verbose_version_info.resource_finders import local_install_basepath
from verbose_version_info.utils import distribution
from verbose_version_info.vcs import VCS_COMMIT_ID_READERS


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


def vv_info(distribution_name: str) -> VerboseVersionInfo:
    """Verbose version information of an installed package.

    Known limitations:
        * Does not include uncommitted changes.
        * Can't determine vcs information for tarball installations.
            E.g. ``pip install https://github.com/s-weigand/git-install-test-distribution/archive/main.zip``

    Parameters
    ----------
    distribution_name : str
        The name of the distribution package as a string.

    Returns
    -------
    VerboseVersionInfo
        Verbose version information of the installed package,
        as detailed as possible.
    """  # noqa: E501
    dist_mtime = dist_info_mtime(distribution_name)
    url_vv_info = find_url_info(distribution_name)
    if url_vv_info is not None and url_vv_info.commit_id and url_vv_info.vcs_name:
        return url_vv_info
    else:
        local_path = local_install_basepath(distribution_name, vv_info=url_vv_info)
        if local_path is not None:
            for vsc_reader in VCS_COMMIT_ID_READERS:
                dist_mtime = dist_mtime or datetime.now()
                vcs_info = vsc_reader(local_path, dist_mtime)
                if vcs_info is not None:
                    return VerboseVersionInfo(
                        release_version=release_version(distribution_name),
                        url=local_path.as_uri(),
                        vcs_name=vcs_info.vcs_name,
                        commit_id=vcs_info.commit_id,
                    )
            return VerboseVersionInfo(
                release_version=release_version(distribution_name),
                url=local_path.as_uri(),
            )

    return VerboseVersionInfo(release_version=release_version(distribution_name))
