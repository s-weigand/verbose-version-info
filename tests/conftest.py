"""Pytest fixturesfor the testsuite."""
import os
from datetime import datetime

import pytest
from _pytest.monkeypatch import MonkeyPatch


@pytest.fixture
def mock_os_stat_mtime(monkeypatch: MonkeyPatch):
    def mock_func(date_obj: datetime):

        timestamp = int(date_obj.timestamp())

        class MockStat:
            st_mtime = timestamp

        monkeypatch.setattr(os, "stat", lambda x: MockStat())

    yield mock_func
