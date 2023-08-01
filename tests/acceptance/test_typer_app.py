"""This module contains the tests for the Typer app."""

from typer.testing import CliRunner

from src.cli.typer_cli import app


def test_hello_command():
    """Test the hello command."""
    runner = CliRunner()
    result = runner.invoke(app, ["hello"])
    assert result.exit_code == 0
    assert (
        result.output == "Hello, world!\nHello, ErgastService!\nHello, GithubService!\n"
    )
