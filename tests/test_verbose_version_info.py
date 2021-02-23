"""Tests for ``verbose_version_info`` package."""

import pytest

from verbose_version_info import SETTINGS
from verbose_version_info import __version__
from verbose_version_info.verbose_version_info import release_version


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
