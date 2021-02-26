"""Pytest fixturesfor the testsuite."""
import os
from copy import copy
from datetime import datetime

import pytest
from _pytest.monkeypatch import MonkeyPatch


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

    yield mock_func
