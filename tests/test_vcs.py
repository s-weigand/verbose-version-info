"""Tests for the ``vcs`` module"""

try:
    from importlib.metadata import PackagePath
except ImportError:
    from importlib_metadata import PackagePath  # type: ignore

from pathlib import Path
from typing import Optional
from typing import Tuple
from typing import Union

import pytest
from _pytest.monkeypatch import MonkeyPatch
from tests import DUMMY_PKG_ROOT
from tests import PKG_ROOT

import verbose_version_info.vcs
import verbose_version_info.verbose_version_info
from verbose_version_info.metadata_compat import Distribution
from verbose_version_info.vcs import VerboseVersionInfo
from verbose_version_info.vcs import add_vcs_commit_id_reader
from verbose_version_info.vcs import get_editable_install_basepath
from verbose_version_info.vcs import get_local_git_commit_id
from verbose_version_info.vcs import get_local_install_basepath
from verbose_version_info.vcs import get_path_of_file_uri
from verbose_version_info.vcs import get_url_vcs_information
from verbose_version_info.vcs import run_vcs_commit_id_command


def test_get_vcs_information_git_install():
    """Vsc information for git+url installed package."""
    result = get_url_vcs_information("git-install-test-distribution")
    expected = VerboseVersionInfo(
        release_version="0.0.2",
        url="https://github.com/s-weigand/git-install-test-distribution.git",
        commit_id="a7f7bf28dbe9bfceba1af8a259383e398a942ad0",
        vcs="git",
    )

    assert result == expected


@pytest.mark.parametrize(
    "distribution_name, version, folder_name",
    (
        ("local-install", "0.0.7", "local_install"),
        ("local_install_with_spaces_in_path", "0.0.8", "local_install with spaces in path"),
        ("local_install_src_pattern", "0.0.9", "local_install_src_pattern"),
        ("local_install_with_dotgit", "0.0.10", "local_install_with_dotgit"),
    ),
)
def test_get_vcs_information_local_installation(
    distribution_name: str, version: str, folder_name: str
):
    """No Vsc information local installed packages w/o vcs."""
    result = get_url_vcs_information(distribution_name)
    expected = VerboseVersionInfo(
        release_version=version,
        url=(DUMMY_PKG_ROOT / folder_name).as_uri(),
        commit_id="",
        vcs="",
    )

    assert result == expected


@pytest.mark.parametrize("distribution_name", ("not-a-distribution", "pytest"))
def test_get_vcs_information_none_url_install(distribution_name: str):
    """Invalid distribution Vcs information."""

    assert get_url_vcs_information(distribution_name) is None


@pytest.mark.parametrize(
    "json_str,expected",
    (
        (
            '{"url": "https://foo.bar"}',
            VerboseVersionInfo(
                release_version="0.0.2",
                url="https://foo.bar",
                commit_id="",
                vcs="",
            ),
        ),
        (
            '{"url": "https://foo.bar", "vcs_info":{"unknown_key":"foo"}}',
            VerboseVersionInfo(
                release_version="0.0.2",
                url="https://foo.bar",
                commit_id="",
                vcs="",
            ),
        ),
        (
            '{"url": "https://foo.bar", "vcs_info":{"commit_id":"foo"}}',
            VerboseVersionInfo(
                release_version="0.0.2",
                url="https://foo.bar",
                commit_id="foo",
                vcs="",
            ),
        ),
    ),
)
def test_get_vcs_information_url_install(
    monkeypatch: MonkeyPatch, json_str: str, expected: VerboseVersionInfo
):
    """Retrieve vsc information for url installed package.
    Reading the text to parse is mocked, so different results can be checked.
    """
    monkeypatch.setattr(PackagePath, "read_text", lambda x: json_str)
    monkeypatch.setattr(
        verbose_version_info.verbose_version_info,
        "get_distribution",
        verbose_version_info.verbose_version_info.get_distribution.__wrapped__,
    )

    result = get_url_vcs_information("git-install-test-distribution")

    assert result == expected


def test_get_vcs_information_url_install_broken_dist(monkeypatch: MonkeyPatch):
    """Distribution files property is None
    I.e. if RECORD for dist-info or SOURCES.txt for egg-info.

    See: importlib.metadata.Distribution.files
    """
    monkeypatch.setattr(Distribution, "files", None)
    monkeypatch.setattr(
        verbose_version_info.verbose_version_info,
        "get_distribution",
        verbose_version_info.verbose_version_info.get_distribution.__wrapped__,
    )

    result = get_url_vcs_information("git-install-test-distribution")

    assert result is None


@pytest.mark.parametrize(
    "distribution_name,expected",
    (
        ("git-install-test-distribution", None),
        ("editable_install_setup_cfg", DUMMY_PKG_ROOT / "editable_install_setup_cfg"),
        ("editable_install_setup_py", DUMMY_PKG_ROOT / "editable_install_setup_py"),
        ("editable_install_src_pattern", DUMMY_PKG_ROOT / "editable_install_src_pattern"),
        ("editable_install_with_dotgit", DUMMY_PKG_ROOT / "editable_install_with_dotgit"),
        ("not-a-distribution", None),
        ("pytest", None),
    ),
)
def test_get_editable_install_basepath(distribution_name: str, expected: str):
    """Find basepath for all editable installed packages."""
    assert get_editable_install_basepath(distribution_name) == expected


@pytest.mark.parametrize(
    "path",
    (
        Path(__file__),
        (DUMMY_PKG_ROOT / "local_install"),
        (DUMMY_PKG_ROOT / "local_install with spaces in path"),
        (DUMMY_PKG_ROOT / "local_install_with_dotgit"),
    ),
)
def test_parse_file_uri(path: Path):
    """Back and forth parsing of existing Paths  returns the original path."""
    uri = path.as_uri()
    result = get_path_of_file_uri(uri)

    assert result == path
    assert result.exists()


@pytest.mark.parametrize(
    "uri",
    (
        "random_string",
        "file:///random_string",
        (Path(__file__) / "does_not_exist").as_uri(),
    ),
)
def test_get_path_of_file_uri(uri: str):
    """Nonsense and invalid path uri's give None."""
    result = get_path_of_file_uri(uri)

    assert result is None


@pytest.mark.parametrize(
    "distribution_name,expected",
    (
        ("git-install-test-distribution", None),
        ("editable_install_setup_cfg", DUMMY_PKG_ROOT / "editable_install_setup_cfg"),
        ("editable_install_setup_py", DUMMY_PKG_ROOT / "editable_install_setup_py"),
        ("editable_install_src_pattern", DUMMY_PKG_ROOT / "editable_install_src_pattern"),
        ("editable_install_with_dotgit", DUMMY_PKG_ROOT / "editable_install_with_dotgit"),
        ("not-a-distribution", None),
        ("pytest", None),
        ("local-install", DUMMY_PKG_ROOT / "local_install"),
        (
            "local_install_with_spaces_in_path",
            DUMMY_PKG_ROOT / "local_install with spaces in path",
        ),
        (
            "local_install_src_pattern",
            DUMMY_PKG_ROOT / "local_install_src_pattern",
        ),
        (
            "local_install_with_dotgit",
            DUMMY_PKG_ROOT / "local_install_with_dotgit",
        ),
    ),
)
def test_get_local_install_basepath(distribution_name: str, expected: str):
    """Validate Path for all locally installed packages."""
    assert get_local_install_basepath(distribution_name) == expected


def test_get_local_install_basepath_with_vv_info_not_none():
    """'get_url_vcs_information' isn't executed if 'vv_info' is passed."""
    expected_path = PKG_ROOT / "tests"
    result = get_local_install_basepath(
        "verbose-version-info",
        vv_info=VerboseVersionInfo(
            release_version="", url=expected_path.as_uri(), commit_id="", vcs=""
        ),
    )
    assert result == expected_path


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
    def dummy(local_install_basepath: Path) -> Optional[Tuple[str, str]]:
        if local_install_basepath.exists():
            return "foo", "bar"
        return None

    assert len(verbose_version_info.vcs.VCS_COMMIT_ID_READER) == 1
    assert dummy in verbose_version_info.vcs.VCS_COMMIT_ID_READER
