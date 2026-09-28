"""Pytest fixturesfor the testsuite."""

import os
from copy import copy
from datetime import datetime

import pytest
from _pytest.monkeypatch import MonkeyPatch
from tests import DUMMY_PKG_ROOT
from tests import MTIME_DATE_NOW

import verbose_version_info.resource_finders


@pytest.fixture
def mock_os_stat_mtime(monkeypatch: MonkeyPatch):
    def mock_func(date_obj: datetime):
        timestamp = int(date_obj.timestamp())

        # Prevent max recursion error
        _stat = copy(os.stat)

        def mock_stat(*args, **kwargs):
            result = _stat(*args, **kwargs)

            class MockStatResult:
                st_mode = result.st_mode
                st_mtime = timestamp

            return MockStatResult()

        monkeypatch.setattr(os, "stat", mock_stat)
        monkeypatch.setattr(
            verbose_version_info.resource_finders, "_datetime_now", lambda: MTIME_DATE_NOW
        )

    yield mock_func


@pytest.fixture
def dirty_vsc_path():
    vsc_root = DUMMY_PKG_ROOT / "editable_install_with_dotgit"
    temp_file = vsc_root / "uncommited_file"
    try:
        temp_file.touch(exist_ok=True)
        yield vsc_root
    finally:
        temp_file.unlink()
