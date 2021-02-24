"""Tests for the ``vcs`` module"""

from pathlib import Path
from typing import Optional
from typing import Tuple
from typing import Union

import pytest
from _pytest.monkeypatch import MonkeyPatch
from tests import DUMMY_PKG_ROOT

import verbose_version_info.vcs
from verbose_version_info.data_containers import VcsInfo
from verbose_version_info.vcs import add_vcs_commit_id_reader
from verbose_version_info.vcs import get_local_git_commit_id
from verbose_version_info.vcs import run_vcs_commit_id_command


@pytest.mark.parametrize(
    "command_str,need_to_exist_path_child,expected",
    (
        ("print('foo')", ".", ("dummy", "foo")),
        ("syntax-error = 1", ".", None),
        ("print(foo)", "none_existing_child", None),
    ),
)
def test_run_vcs_commit_id_command(command_str: str, need_to_exist_path_child: str, expected: str):
    """Different execution path:
    - success
    - missing path child
    - command error
    """
    result = run_vcs_commit_id_command(
        vcs_name="dummy",
        commit_id_command=("python", "-c", f"{command_str}"),
        local_install_basepath=DUMMY_PKG_ROOT / "editable_install_with_dotgit",
        need_to_exist_path_child=need_to_exist_path_child,
    )

    assert result == expected


@pytest.mark.parametrize(
    "local_install_basepath,expected",
    (
        (DUMMY_PKG_ROOT / "local_install_src_pattern", None),
        (
            DUMMY_PKG_ROOT / "editable_install_with_dotgit",
            ("git", "f2d32d41644de04122e478d6ef9639f5c2292eca"),
        ),
        (
            DUMMY_PKG_ROOT / "local_install_with_dotgit",
            ("git", "df5c1e9302972fa5732a320d4cdef478cf783b8f"),
        ),
    ),
)
def test_get_local_git_commit_id(
    local_install_basepath: Path, expected: Union[Tuple[str, str], None]
):
    """git commit_id for locally installed packages"""
    assert get_local_git_commit_id(local_install_basepath) == expected


def test_add_vcs_commit_id_reader(monkeypatch: MonkeyPatch):
    """Decorated function get added as supposed."""
    monkeypatch.setattr(verbose_version_info.vcs, "VCS_COMMIT_ID_READER", [])

    @add_vcs_commit_id_reader
    def dummy(local_install_basepath: Path) -> Optional[VcsInfo]:
        if local_install_basepath.exists():
            return VcsInfo(vcs_name="foo", commit_id="bar")
        return None

    assert len(verbose_version_info.vcs.VCS_COMMIT_ID_READER) == 1
    assert dummy in verbose_version_info.vcs.VCS_COMMIT_ID_READER
