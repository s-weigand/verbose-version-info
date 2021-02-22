"""Tests for the CLI"""
import sys

import pytest
from _pytest.monkeypatch import MonkeyPatch
from click.testing import CliRunner

from verbose_version_info import cli


def test_missing_cli_extra_requires(monkeypatch: MonkeyPatch):
    """Exception raised if cli extra_requires is missing"""
    monkeypatch.delitem(sys.modules, "verbose_version_info.cli")
    monkeypatch.setitem(sys.modules, "click", None)

    with pytest.raises(ImportError, match=r"pip install verbose-version-info\[cli\]"):
        import verbose_version_info.cli  # noqa: F401


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert "Not yet Implemented!" in result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output
