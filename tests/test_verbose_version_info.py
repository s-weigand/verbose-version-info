"""Tests for ``verbose_version_info`` package."""

import pytest
from tests import DUMMY_PKG_ROOT

from verbose_version_info import SETTINGS
from verbose_version_info import __version__
from verbose_version_info.data_containers import VerboseVersionInfo
from verbose_version_info.verbose_version_info import release_version
from verbose_version_info.verbose_version_info import vv_info


@pytest.mark.parametrize(
    "distribution_name,expected",
    (
        ("verbose-version-info", __version__),
        ("verbose_version_info", __version__),
        ("git-install-test-distribution", "0.0.2"),
        ("git_install_test_distribution", "0.0.2"),
        ("editable_install_setup_cfg", "0.0.3"),
        ("editable_install_setup_py", "0.0.4"),
        ("editable_install_src_pattern", "0.0.6"),
        ("editable_install_with_dotgit", "0.0.5"),
        ("local_install", "0.0.7"),
        ("local_install_with_spaces_in_path", "0.0.8"),
        ("local_install_src_pattern", "0.0.9"),
        ("local_install_with_dotgit", "0.0.10"),
        ("not-a-distribution", "Unknown"),
    ),
)
def test_release_version(distribution_name: str, expected: str):
    """Versions for dummy packages and root.
    Missing package has default version string."""
    assert release_version(distribution_name) == expected


def test_changing_not_found_version_str(monkeypatch):
    """Changed setting 'not_found_version_str' changes version string."""
    monkeypatch.setitem(SETTINGS, "not_found_version_str", "Not Installed")

    assert release_version("not-a-distribution") == "Not Installed"


@pytest.mark.parametrize(
    "distribution_name, expected",
    (
        (
            "git_install_test_distribution",
            VerboseVersionInfo(
                release_version="0.0.2",
                url="https://github.com/s-weigand/git-install-test-distribution.git",
                commit_id="a7f7bf28dbe9bfceba1af8a259383e398a942ad0",
                vcs_name="git",
            ),
        ),
        (
            "editable_install_with_dotgit",
            VerboseVersionInfo(
                release_version="0.0.5",
                url=(DUMMY_PKG_ROOT / "editable_install_with_dotgit").as_uri(),
                commit_id="f3c8d36715f7cd14dc73e6b3ae76cb2669c97b5f",
                vcs_name="git",
            ),
        ),
        (
            "local_install_with_dotgit",
            VerboseVersionInfo(
                release_version="0.0.10",
                url=(DUMMY_PKG_ROOT / "local_install_with_dotgit").as_uri(),
                commit_id="ff76038f76fcc106885cb9f19748e989d7d862b9",
                vcs_name="git",
            ),
        ),
        (
            "editable_install_setup_py",
            VerboseVersionInfo(
                release_version="0.0.4",
                url=(DUMMY_PKG_ROOT / "editable_install_setup_py").as_uri(),
            ),
        ),
        (
            "pytest",
            VerboseVersionInfo(
                release_version=pytest.__version__,
            ),
        ),
    ),
)
def test_verbose_version_info(distribution_name: str, expected: VerboseVersionInfo):
    """ "Verbose version for differently installed packages.
    - Installed from url with vcs (git_install_test_distribution)
    - Editable installed with vcs (editable_install_with_dotgit)
    - Source installed with vcs (local_install_with_dotgit)
    - Editable installed no vcs (editable_install_setup_py)
    - PyPi installed (pytest)

    """
    result = vv_info(distribution_name)

    assert result == expected
