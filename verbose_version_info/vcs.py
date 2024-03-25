"""Module containing code for version control system retrieval."""

import subprocess
from datetime import datetime
from pathlib import Path
from typing import Callable
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union
from warnings import warn

from verbose_version_info.data_containers import VcsInfo
from verbose_version_info.settings import VCS_SETTINGS

VcsCommitIdReader = Callable[[Path, datetime], Optional[VcsInfo]]

VCS_COMMIT_ID_READERS: List[VcsCommitIdReader] = []


class UncommittedChangesWarning(UserWarning):
    """Warning thrown if a director under source control has uncommitted changes."""

    pass


def add_vcs_commit_id_reader(func: VcsCommitIdReader) -> VcsCommitIdReader:
    """Add vcs commit_id reader function to the list of registered function.

    This is pretty much the most simple decorator possible,
    there isn't any sanity checking (e.g. functools function signature)
    since this package doesn't have a pluginsystem and the sanity check is done by mypy.

    Parameters
    ----------
    func : VcsCommitIdReader
        Function to be added

    Returns
    -------
    VcsCommitIdReader
        Originally added function.
    """
    VCS_COMMIT_ID_READERS.append(func)

    return func


def run_vcs_commit_id_command(
    *,
    vcs_name: str,
    commit_id_command: Union[List[str], Tuple[str, ...]],
    local_install_basepath: Path,
    need_to_exist_path_child: str = ".",
    check_dirty_command: Optional[Union[List[str], Tuple[str, ...]]] = None,
) -> Optional[VcsInfo]:
    """Inner function of commit_id retrieval functions.

    Parameters
    ----------
    vcs_name : str
        Name if the vcs, which will be used as part of the result.
    commit_id_command : Union[List[str], Tuple[str, ...]]
        Shell command to return the commit_id.
        E.g. for ``git``: ``("git", "log", "--before", f"'{date_string}'", "-n", "1", "--pretty=format:%H",)``
    local_install_basepath : Path
        Basepath of the local installation.
    need_to_exist_path_child : str
        Childitem that needs to exists inside of local_install_basepath.
        E.g. for ``git``: ``".git"``. by default "."
    check_dirty_command : Optional[Union[List[str], Tuple[str, ...]]]
        Command to be run for checking if a directory contains uncommitted changes.
        E.g. for ``git``: ``("git", "status", "-s")``by default None

    Returns
    -------
    Optional[VcsInfo]
        (vcs_name, commit_id)

    See Also
    --------
    get_local_git_commit_id
    """  # noqa: E501
    if (local_install_basepath / need_to_exist_path_child).exists():
        if check_dirty_command is not None and VCS_SETTINGS["warn_dirty"] is True:
            is_dirty_output = subprocess.run(
                check_dirty_command, cwd=local_install_basepath, stdout=subprocess.PIPE
            )
            is_dirt = is_dirty_output.stdout.decode().rstrip()
            if is_dirt != "":
                warn(
                    UncommittedChangesWarning(
                        f"The package installed from source at {local_install_basepath!r}, "
                        " contains uncommitted changes."
                    )
                )

        vcs_output = subprocess.run(
            commit_id_command, cwd=local_install_basepath, stdout=subprocess.PIPE
        )
        commit_id = vcs_output.stdout.decode().rstrip()
        if vcs_output.returncode == 0 and commit_id != "":
            return VcsInfo(vcs_name=vcs_name, commit_id=commit_id)
    return None


@add_vcs_commit_id_reader
def local_git_commit_id(local_install_basepath: Path, dist_mtime: datetime) -> Optional[VcsInfo]:
    """Get git commit_id of locally installed package.

    Parameters
    ----------
    local_install_basepath : Path
        Basepath of the local installation.
    dist_mtime: datetime
        Time the packaged distribution was modified.
        This is only important for none editable installations from source.

    Returns
    -------
    Optional[VcsInfo]
        (vcs_name, commit_id)

    See Also
    --------
    run_vcs_commit_id_command
    verbose_version_info.resource_finders.dist_info_mtime
    """
    date_string = dist_mtime.strftime("%Y-%m-%d %H:%M:%S")
    return run_vcs_commit_id_command(
        vcs_name="git",
        commit_id_command=(
            "git",
            "log",
            "--before",
            f"'{date_string}'",
            "-n",
            "1",
            "--pretty=format:%H",
        ),
        local_install_basepath=local_install_basepath,
        need_to_exist_path_child=".git",
        check_dirty_command=("git", "status", "-s"),
    )
