"""Unit test package for verbose_version_info."""

from datetime import datetime
from pathlib import Path

TESTS_ROOT = Path(__file__).parent
PKG_ROOT = TESTS_ROOT.parent
DUMMY_PKG_ROOT = TESTS_ROOT / "dummy_packages"


MTIME_DATE_PAST = datetime(2021, 2, 24)

MTIME_DATE_NOW = datetime.now().replace(microsecond=0)
