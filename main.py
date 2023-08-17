"""This module contains the entry point for the Lyzer-ETL application."""

# System imports
from sys import argv

# Third-party imports
from rich import print as rich_print

# Local imports
from src.api.github_service import GithubService
from src.config.configuration import read_config
from src.cli.typer_cli import app
from src.helpers.utilities import read_version_file, update_now


def main() -> None:
    """
    Entry point for the Lyzer-ETL application.

    This function is the entry point for the Lyzer-ETL application. It is
    responsible for setting up the application, updating it if necessary, and
    running the CLI.
    """
    if argv[0] != "main.py":
        update()
    else:
        rich_print("[yellow]Running in development mode.[/yellow]")

    app()


def update() -> None:
    """
    Update the application.

    This function is responsible for updating the application. It does this by
    reading the version file and the configuration file, and then passing them
    to the GithubService class. The GithubService class is responsible for
    checking if an update is available, and if so, downloading and installing
    it.
    """
    version = read_version_file()
    config = read_config()
    service = GithubService(config, version)
    update_now(service)


if __name__ == "__main__":
    main()
