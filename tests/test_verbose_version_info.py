"""Tests for ``verbose_version_info`` package."""

from pathlib import Path

import pytest

from verbose_version_info import SETTINGS
from verbose_version_info import __version__
from verbose_version_info.metadata_compat import distribution
from verbose_version_info.verbose_version_info import NotFoundDistribution
from verbose_version_info.verbose_version_info import basic_version
from verbose_version_info.verbose_version_info import get_distribution


def test_get_distribution():
    """Valid distribution."""
    result = get_distribution("verbose-version-info")
    expected = distribution("verbose-version-info")

    assert result.version == expected.version
    assert result.files == expected.files
    assert result.requires == expected.requires


def test_get_distribution_not_found():
    """Invalid distribution."""
    result = get_distribution("not-a-distribution")

    assert isinstance(result, NotFoundDistribution)
    assert result.version == "Unknown"
    assert result.files == []
    assert result.requires == []

    # Just for coverage of NotFoundDistribution
    assert result.read_text("foo") is None
    assert result.locate_file("foo") == Path("foo")
    assert result.locate_file(Path("foo")) == Path("foo")


@pytest.mark.parametrize(
    "distribution_name,expected",
    (
        ("verbose-version-info", __version__),
        ("verbose_version_info", __version__),
        ("git-install-test-distribution", "0.0.2"),
        ("git_install_test_distribution", "0.0.2"),
        ("not-a-distribution", "Unknown"),
    ),
)
def test_basic_version(distribution_name: str, expected: str):
    """Expected default behavior with default settings."""
    assert basic_version(distribution_name) == expected


def test_changing_not_found_version_str(monkeypatch):
    """Changed setting 'not_found_version_str' changes version string."""
    monkeypatch.setitem(SETTINGS, "not_found_version_str", "Not Installed")

    assert basic_version("not-a-distribution") == "Not Installed"
