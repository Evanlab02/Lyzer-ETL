"""This module contains the tests for the Typer app."""

from typer.testing import CliRunner

from src.cli.typer_cli import app
from src.helpers.utilities import read_version_file


def test_version_command() -> None:
    """
    Test the version command.

    This will test the version command by running the command and checking the
    output.
    """
    runner = CliRunner()
    result = runner.invoke(app, ["version"])
    version = read_version_file()
    assert result.output == f"Lyzer-ETL version {version}\n"
    assert result.exit_code == 0
