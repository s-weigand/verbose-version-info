#!/usr/bin/env python

"""Tests for `verbose_version_info` package."""

# import pytest

from verbose_version_info import __version__
from verbose_version_info.verbose_version_info import basic_version


def test_basic_version():
    """Sample pytest test function with the pytest fixture as an argument."""
    assert basic_version("verbose-version-info") == __version__
