"""This module contains the entry point for the Lyzer-ETL application."""

from sys import argv

from rich import print as rich_print

# Local imports
from src.api.github_service import GithubService
from src.config.configuration import setup_app, read_config
from src.cli.typer_cli import app
from src.helpers.utilities import read_version_file, update_now


def main():
    """Entry point for the Lyzer-ETL application."""
    setup_app()

    if argv[0] != "main.py":
        update()
    else:
        rich_print("[yellow]Running in development mode.[/yellow]")

    app()


def update():
    """Update the application."""
    version = read_version_file()
    config = read_config()
    service = GithubService(config, version)
    update_now(service)


if __name__ == "__main__":
    main()
