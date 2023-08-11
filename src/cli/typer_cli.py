"""This module contains the typer CLI app and logic for the Lyzer-ETL application."""

import typer
from rich import print as rich_print

from src.api.github_service import GithubService
from src.config.configuration import read_config
from src.helpers.utilities import read_version_file

app = typer.Typer()


@app.command()
def update():
    """Update the application."""
    config = read_config()
    version = read_version_file()
    github_service = GithubService(config, version)
    github_service.update_app(True)


@app.command()
def version():
    """Version command."""
    version = read_version_file()
    rich_print(f"Lyzer-ETL version {version}")
