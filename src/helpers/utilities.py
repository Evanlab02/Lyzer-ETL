"""
This module contains all utility functions for the Lyzer-ETL application.

Functions:
    read_version_file: Read the version file.
    update_now: Update the application.
"""

import os
import sys

from src.error.exceptions import GithubRequestError


def read_version_file():
    """
    Read the version file.

    This function will read the version file and return the version number.
    It will determine if it is running as a executable or as a script.

    Returns:
        str: The version number.
    """
    base_path = ""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    try:
        with open(f"{base_path}/version.txt", "r", encoding="UTF-8") as version_file:
            return version_file.read().strip().replace("\n", "")
    except FileNotFoundError:
        return "0.0.0"


def update_now(github_service):
    """
    Update the application.

    This function will update the application by calling the update_app method
    from the GithubService class and handling any errors that may occur.

    Args:
        github_service (GithubService): The GithubService class.

    Raises:
        GithubRequestError: Raised when a request to the Github API fails.
    """
    try:
        github_service.update_app()
    except GithubRequestError as error:
        print(f"Github request failed with status code {error.status_code}.")
