"""This module contains all utility functions for the Lyzer-ETL application."""

import os
import sys

from src.error.exceptions import GithubRequestError


def read_version_file():
    """Read the version file."""
    base_path = ""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = {sys._MEIPASS}
    except Exception:
        base_path = os.path.abspath(".")

    try:
        with open(f"{base_path}/version.txt", "r", encoding="UTF-8") as version_file:
            return version_file.read().strip().replace("\n", "")
    except FileNotFoundError:
        return "0.0.0"


def update_now(github_service):
    """Update the application."""
    try:
        github_service.update_app()
    except GithubRequestError as error:
        print(f"Github request failed with status code {error.status_code}.")
