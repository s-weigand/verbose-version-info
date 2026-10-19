"""Tests for the CLI"""

import re
import sys

import pytest
from _pytest.monkeypatch import MonkeyPatch
from typer.testing import CliRunner

from verbose_version_info.cli import cli


def test_missing_cli_extra_requires(monkeypatch: MonkeyPatch):
    """Exception raised if cli extra_requires is missing"""
    monkeypatch.delitem(sys.modules, "verbose_version_info.cli")
    monkeypatch.setitem(sys.modules, "typer", None)

    with pytest.raises(ImportError, match=r"pip install verbose-version-info\[cli\]"):
        import verbose_version_info.cli  # noqa: F401


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0
    assert "Not yet Implemented!" in result.output
    help_result = runner.invoke(cli, ["--help"])
    assert help_result.exit_code == 0
    assert re.search(r"--help\s+Show this message and exit\.", help_result.output) is not None
