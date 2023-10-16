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
from src.config.configuration import read_config, get_connection_string, write_config
from src.helpers.utilities import read_version_file

app = typer.Typer(pretty_exceptions_show_locals=False)
app_version = read_version_file()
config = read_config()
github_service = GithubService(config, app_version)

app.add_typer(load_app, name="load")


@app.command()
def update() -> None:
    """
    Update the application.

    This will check the config file to see when last there was a check for a new update.
    If the last check was more than 24 hours ago, it will check for a new update.
    If there is a new update, it will download the new version in the home directory.
    """
    github_service.update_app(True)


@app.command()
def version() -> None:
    """
    Display the version of the application.

    This will read the version file and print the version of the application.
    """
    version = read_version_file()
    rich_print(f"Lyzer-ETL version {version}")


@app.command()
def config() -> None:
    """
    Gives the user the option to rewrite their config Mongo Connection URI

    If they select yes, they will be able to rewrite their URI
    """
    config = read_config()
    connection_uri = config["mongoUri"]
    rich_print(f"\nYour current Mongo Connection String is: [green]{connection_uri}[/green]")

    options = ["y", "yes", "n", "no"]
    
    while True:
        option = input("\nWould you like to update your connection string? (y/n): ").strip().lower()

        if option in options:
            break
    
    if option == "y" or option == "yes":
        config = get_connection_string(config)
        write_config(config)