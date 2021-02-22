"""Tests for the ``vcs`` module"""

try:
    from importlib.metadata import PackagePath
except ImportError:
    from importlib_metadata import PackagePath  # type: ignore

from pathlib import Path

import pytest
from _pytest.monkeypatch import MonkeyPatch
from tests import DUMMY_PKG_ROOT
from tests import PKG_ROOT

import verbose_version_info.verbose_version_info
from verbose_version_info.metadata_compat import Distribution
from verbose_version_info.vcs import VerboseVersionInfo
from verbose_version_info.vcs import get_editable_install_basepath
from verbose_version_info.vcs import get_local_install_basepath
from verbose_version_info.vcs import get_path_of_file_uri
from verbose_version_info.vcs import get_url_vcs_information


def test_get_vcs_information_git_install():
    """Vsc information for git+url installed package."""
    result = get_url_vcs_information("git-install-test-distribution")
    expected = VerboseVersionInfo(
        version="0.0.2",
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
        version=version,
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
                version="0.0.2",
                url="https://foo.bar",
                commit_id="",
                vcs="",
            ),
        ),
        (
            '{"url": "https://foo.bar", "vcs_info":{"unknown_key":"foo"}}',
            VerboseVersionInfo(
                version="0.0.2",
                url="https://foo.bar",
                commit_id="",
                vcs="",
            ),
        ),
        (
            '{"url": "https://foo.bar", "vcs_info":{"commit_id":"foo"}}',
            VerboseVersionInfo(
                version="0.0.2",
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
        ("verbose-version-info", PKG_ROOT),
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
    """'get_url_vcs_information' isn't executed if 'vv_info' passed."""
    expected_path = PKG_ROOT / "tests"
    result = get_local_install_basepath(
        "verbose-version-info",
        vv_info=VerboseVersionInfo(version="", url=expected_path.as_uri(), commit_id="", vcs=""),
    )
    assert result == expected_path
