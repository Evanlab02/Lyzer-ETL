"""
This module contains all utility functions for the Lyzer-ETL application.

Functions:
    read_version_file: Read the version file.
    update_now: Update the application.
"""

import os
import sys
from datetime import datetime

from rich.table import Table

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
        print(f"[red]HTTP Error: {error.status_code}.[/red]")
        print("[red]Could not check for updates.[/red]")


def validate_year(year: int | str, allow_future: bool = False) -> int:
    """
    Validate the year.

    This function will validate the year given by the user to ensure that it
    is a valid formula 1 season.

    The allow future argument will allow the user to specify a year that is
    one year in the future. This is used when loading the schedule data.

    Args:
        year (int | str): The year to validate.

    Returns:
        int: The year that was validated. If the year was a string, it will be
            converted to an integer.

    Raises:
        ValueError: Raised when the year is not valid.
    """
    MIN_YEAR = 1950
    MAX_YEAR = datetime.now().year + (1 if allow_future else 0)

    if isinstance(year, str):
        year = int(year)

    if year not in range(MIN_YEAR, MAX_YEAR + 1):
        raise ValueError(f"Year must be between {MIN_YEAR} and {MAX_YEAR}.")

    return year


def generate_table(data: list[dict] | dict):
    """
    Generate a table from the data given.

    This function will generate a table from the data given. It will only
    display the fields that are strings, integers, floats or booleans.

    Args:
        data (list[dict] | dict): The data to generate the table from.

    Returns:
        Table | str: The table that was generated or a string if there was no
            data to display.
    """
    table = Table(
        title="Summarized Data (NOTE: Not all fields can be displayed)",
        show_header=True,
        header_style="bold magenta",
    )

    data = data if isinstance(data, list) else [data]
    display_data = []

    if len(data) == 0:
        return "[yellow]No data to display.[/yellow]"

    for item in data:
        display_item = {}
        for key, value in item.items():
            if not isinstance(value, (str, int, float, bool)):
                continue
            display_item[key] = str(value)
        display_data.append(display_item)

    for key in display_data[0].keys():
        table.add_column(key)

    for item in display_data:
        table.add_row(*item.values())

    return table
