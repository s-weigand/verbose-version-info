import os
from datetime import datetime
from pathlib import Path

import pytest
from _pytest.monkeypatch import MonkeyPatch
from tests import DUMMY_PKG_ROOT
from tests import PKG_ROOT

import verbose_version_info.utils
from verbose_version_info.data_containers import VerboseVersionInfo
from verbose_version_info.metadata_compat import PackagePath
from verbose_version_info.resource_finders import dist_info_mtime
from verbose_version_info.resource_finders import egg_link_lines
from verbose_version_info.resource_finders import file_uri_to_path
from verbose_version_info.resource_finders import find_editable_install_basepath
from verbose_version_info.resource_finders import find_url_info
from verbose_version_info.resource_finders import local_install_basepath


def test_find_url_info_git_install():
    """Vsc information for git+url installed package."""
    result = find_url_info("git-install-test-distribution")
    expected = VerboseVersionInfo(
        release_version="0.0.2",
        url="https://github.com/s-weigand/git-install-test-distribution.git",
        commit_id="a7f7bf28dbe9bfceba1af8a259383e398a942ad0",
        vcs_name="git",
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
def test_find_url_info_local_installation(distribution_name: str, version: str, folder_name: str):
    """No Vsc information local installed packages w/o vcs."""
    result = find_url_info(distribution_name)
    expected = VerboseVersionInfo(
        release_version=version,
        url=(DUMMY_PKG_ROOT / folder_name).as_uri(),
    )

    assert result == expected


@pytest.mark.parametrize("distribution_name", ("not-a-distribution", "pytest"))
def test_find_url_info_none_url_install(distribution_name: str):
    """Not url installed distribution."""

    assert find_url_info(distribution_name) is None


@pytest.mark.parametrize(
    "json_str,expected",
    (
        (
            '{"url": "https://foo.bar"}',
            VerboseVersionInfo(
                release_version="0.0.2",
                url="https://foo.bar",
            ),
        ),
        (
            '{"url": "https://foo.bar", "vcs_info":{"unknown_key":"foo"}}',
            VerboseVersionInfo(
                release_version="0.0.2",
                url="https://foo.bar",
            ),
        ),
        (
            '{"url": "https://foo.bar", "vcs_info":{"commit_id":"foo"}}',
            VerboseVersionInfo(
                release_version="0.0.2",
                url="https://foo.bar",
                commit_id="foo",
            ),
        ),
    ),
)
def test_find_url_info_url_install(
    monkeypatch: MonkeyPatch, json_str: str, expected: VerboseVersionInfo
):
    """Retrieve url information for url installed package.
    Reading the text to parse is mocked, so different results can be checked.
    """
    monkeypatch.setattr(PackagePath, "read_text", lambda x: json_str)
    monkeypatch.setattr(
        verbose_version_info.utils,
        "distribution",
        verbose_version_info.utils.distribution.__wrapped__,
    )

    result = find_url_info("git-install-test-distribution")

    assert result == expected


@pytest.mark.parametrize(
    "distribution_name,expected",
    (
        ("git-install-test-distribution", None),
        (
            "editable_install_setup_cfg",
            [str((DUMMY_PKG_ROOT / "editable_install_setup_cfg").resolve()), "."],
        ),
        (
            "editable_install_setup_py",
            [str((DUMMY_PKG_ROOT / "editable_install_setup_py").resolve()), "."],
        ),
        (
            "editable_install_src_pattern",
            [str((DUMMY_PKG_ROOT / "editable_install_src_pattern" / "src").resolve()), "../"],
        ),
        (
            "editable_install_with_dotgit",
            [str((DUMMY_PKG_ROOT / "editable_install_with_dotgit").resolve()), "."],
        ),
        ("not-a-distribution", None),
        ("pytest", None),
    ),
)
def test_egg_link_lines(distribution_name: str, expected: str):
    """Lines of the egglinkfile for editable installations."""
    assert egg_link_lines(distribution_name) == expected


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
def test_find_editable_install_basepath(distribution_name: str, expected: str):
    """Find basepath for all editable installed packages."""
    assert find_editable_install_basepath(distribution_name) == expected


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
    result = file_uri_to_path(uri)

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
def test_file_uri_to_path(uri: str):
    """Nonsense and invalid path uri's give None."""
    result = file_uri_to_path(uri)

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
def test_local_install_basepath(distribution_name: str, expected: str):
    """Validate Path for all locally installed packages."""
    assert local_install_basepath(distribution_name) == expected


def test_local_install_basepath_with_vv_info_not_none():
    """'get_url_vcs_information' isn't executed if 'vv_info' is passed."""
    expected_path = PKG_ROOT / "tests"
    result = local_install_basepath(
        "verbose-version-info",
        vv_info=VerboseVersionInfo(release_version="", url=expected_path.as_uri()),
    )
    assert result == expected_path


@pytest.mark.parametrize(
    "distribution_name,expected",
    (
        ("git-install-test-distribution", datetime.fromtimestamp(0)),
        ("local_install", datetime.fromtimestamp(0)),
        ("local_install_with_spaces_in_path", datetime.fromtimestamp(0)),
        ("local_install_src_pattern", datetime.fromtimestamp(0)),
        ("local_install_with_dotgit", datetime.fromtimestamp(0)),
        ("editable_install_setup_py", None),
        ("not-a-distribution", None),
    ),
)
def test_dist_info_mtime(monkeypatch: MonkeyPatch, distribution_name: str, expected: str):
    """Since the mtime of the dummy packages can't be controlled it needs to be mocked."""

    class MockStat:
        st_mtime = 0

    monkeypatch.setattr(os, "stat", lambda x: MockStat())

    result = dist_info_mtime(distribution_name)

    assert result == expected
