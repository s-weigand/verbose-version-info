"""Unit test package for verbose_version_info."""
from datetime import datetime
from pathlib import Path

TESTS_ROOT = Path(__file__).parent
PKG_ROOT = TESTS_ROOT.parent
DUMMY_PKG_ROOT = TESTS_ROOT / "dummy_packages"

DUMMY_MTIME_DATE = datetime.fromtimestamp(0)
