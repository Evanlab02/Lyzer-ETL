"""This module contains the entry point for the Lyzer-ETL application."""

from src.cli.typer_cli import app
from src.config.configuration import setup_app


def main():
    """Entry point for the Lyzer-ETL application."""
    setup_app()
    app()


if __name__ == "__main__":
    main()
