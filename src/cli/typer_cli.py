"""
This module contains the typer CLI app and logic for the Lyzer-ETL application.

Commands:
    update: Update the application.
    version: Print the current version of the application.
"""

# Third Party Imports
import typer
from rich import print as rich_print

# Local Imports
from src.api.github_service import GithubService
from src.cli.load_cli import load_app
from src.config.configuration import read_config
from src.error.exceptions import GithubRequestError
from src.helpers.utilities import read_version_file

app = typer.Typer(pretty_exceptions_show_locals=False)
app.add_typer(load_app, name="load")


@app.command()
def update() -> None:
    """
    Update the application.

    This will check the config file to see when last there was a check for a new update.
    If the last check was more than 24 hours ago, it will check for a new update.
    If there is a new update, it will download the new version in the home directory.
    """
    try:
        config = read_config()
        version = read_version_file()
        github_service = GithubService(config, version)
        github_service.update_app(True)
    except GithubRequestError as error:
        rich_print(f"[red]HTTP Error:[/red] {error.status_code}")
        rich_print("[red]Could not check for updates.[/red]")


@app.command()
def version() -> None:
    """
    Display the version of the application.

    This will read the version file and print the version of the application.
    """
    version = read_version_file()
    rich_print(f"Lyzer-ETL version {version}")
