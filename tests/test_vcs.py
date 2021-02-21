"""Tests for the ``vcs`` module"""

try:
    from importlib.metadata import PackagePath
except ImportError:
    from importlib_metadata import PackagePath  # type: ignore

import pytest
from _pytest.monkeypatch import MonkeyPatch
from tests import DUMMY_PKG_ROOT

from verbose_version_info.metadata_compat import Distribution
from verbose_version_info.vcs import VcsInfo
from verbose_version_info.vcs import get_editable_install_basepath
from verbose_version_info.vcs import get_url_vcs_information


def test_get_vcs_information_git_install():
    """Retrieve vsc information for url installed package."""
    result = get_url_vcs_information("git-install-test-distribution")
    expected = VcsInfo(
        url="https://github.com/s-weigand/git-install-test-distribution.git",
        commit_id="a7f7bf28dbe9bfceba1af8a259383e398a942ad0",
        vcs="git",
    )

    assert result == expected


def test_get_vcs_information_local():
    """Retrieve vsc information for url installed package."""
    result = get_url_vcs_information("local-install")
    expected = VcsInfo(
        url=(DUMMY_PKG_ROOT / "local_install").as_uri(),
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
            VcsInfo(
                url="https://foo.bar",
                commit_id="",
                vcs="",
            ),
        ),
        (
            '{"url": "https://foo.bar", "vcs_info":{"unknown_key":"foo"}}',
            VcsInfo(
                url="https://foo.bar",
                commit_id="",
                vcs="",
            ),
        ),
        (
            '{"url": "https://foo.bar", "vcs_info":{"commit_id":"foo"}}',
            VcsInfo(
                url="https://foo.bar",
                commit_id="foo",
                vcs="",
            ),
        ),
    ),
)
def test_get_vcs_information_url_install(
    monkeypatch: MonkeyPatch, json_str: str, expected: VcsInfo
):
    """Retrieve vsc information for url installed package."""
    monkeypatch.setattr(PackagePath, "read_text", lambda x: json_str)

    result = get_url_vcs_information("git-install-test-distribution")

    assert result == expected


def test_get_vcs_information_url_install_broken_dist(monkeypatch: MonkeyPatch):
    """I.e. if RECORD for dist-info or SOURCES.txt for egg-info.

    See: importlib.metadata.Distribution.files
    """
    monkeypatch.setattr(Distribution, "files", None)

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
    """Expected default behavior with default settings."""
    assert get_editable_install_basepath(distribution_name) == expected
