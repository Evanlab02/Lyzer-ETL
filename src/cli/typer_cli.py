"""This module contains the typer CLI app and logic for the Lyzer-ETL application."""

import typer

from api.ergast_service import hello_ergast_service
from api.github_service import hello_github_service

app = typer.Typer()


@app.command()
def hello():
    """Hello command."""
    print("Hello, world!")
    hello_ergast_service()
    hello_github_service()


@app.command()
def goodbye():
    """Goodbye command."""
    print("Goodbye, world!")
