"""This module contains the entry point for the Lyzer-ETL application."""

# Local imports
from src.cli.typer_cli import app


def main() -> None:
    """
    Entry point for the Lyzer-ETL application.

    This will call the Typer CLI app.
    """
    app()


if __name__ == "__main__":
    main()
