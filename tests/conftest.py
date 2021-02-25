"""Pytest fixturesfor the testsuite."""
import os

import pytest
from _pytest.monkeypatch import MonkeyPatch


@pytest.fixture
def mocked_os_stat_mtime(monkeypatch: MonkeyPatch):
    class MockStat:
        st_mtime = 0

    monkeypatch.setattr(os, "stat", lambda x: MockStat())
    yield
