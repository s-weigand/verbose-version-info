"""Tests for verbose_version_info.utils"""

from importlib.metadata import Distribution
from importlib.metadata import distribution as _distribution
from pathlib import Path

import pytest
from _pytest.monkeypatch import MonkeyPatch

import verbose_version_info.utils
from verbose_version_info.utils import NotFoundDistribution
from verbose_version_info.utils import dist_files
from verbose_version_info.utils import distribution


@pytest.mark.parametrize(
    "distribution_name",
    (
        "verbose-version-info",
        "editable_install_src_pattern",
        "editable_install_setup_cfg",
        "editable_install_src_pattern",
    ),
)
def test_distribution(distribution_name: str):
    """Valid distributions."""
    result = distribution(distribution_name)
    expected = _distribution(distribution_name)

    assert result.version == expected.version
    assert result.files == expected.files
    assert result.requires == expected.requires


def test_distribution_not_found():
    """Invalid distribution."""
    result = distribution("not-a-distribution")

    assert isinstance(result, NotFoundDistribution)
    assert result.version == "Unknown"
    assert result.files == []
    assert result.requires == []

    # Just for coverage of NotFoundDistribution
    assert result.read_text("foo") is None
    assert result.locate_file("foo") == Path("foo")
    assert result.locate_file(Path("foo")) == Path("foo")


def test_dist_files(monkeypatch: MonkeyPatch):
    found_files = dist_files("verbose-version-info")

    assert isinstance(found_files, list)
    assert len(found_files) > 0

    no_package_files = dist_files("not-a-distribution")

    assert no_package_files == []

    monkeypatch.setattr(Distribution, "files", None)
    monkeypatch.setattr(
        verbose_version_info.utils,
        "distribution",
        verbose_version_info.utils.distribution.__wrapped__,
    )

    broken_package_files = dist_files("verbose-version-info")

    assert broken_package_files == []
