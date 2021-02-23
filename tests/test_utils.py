"""Tests for verbose_version_info.utils"""

from pathlib import Path

import pytest

from verbose_version_info.metadata_compat import _distribution
from verbose_version_info.utils import NotFoundDistribution
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
