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

from src.models.schedules import Schedule


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


def validate_year(year: int, allow_future: bool = False):
    """
    Validate a year.

    Args:
        year (int): The year to validate.
        allow_future (bool, optional): Allow future year, one year ahead of
            current year. Defaults to False.

    Raises:
        ValueError: If year is not between 1950 and current year or current year + 1.
    """
    current_year = datetime.now().year
    min_year = 1950
    max_year = current_year + 1 if allow_future else 0

    if year not in range(min_year, max_year + 1):
        raise ValueError(f"Year must be between {min_year} and {max_year}.")


def generate_schedules_table(schedules: list[Schedule]) -> Table:
    """
    Generate a schedules table.

    Args:
        schedules (list[Schedule]): List of schedules.

    Returns:
        Table: A schedules table.
    """
    headers = [
        "Round",
        "Race",
        "Race date",
        "Race time",
        "Qualifying date",
        "Qualifying time",
        "Sprint date",
        "Sprint time",
    ]

    table = Table(title="Schedules", show_header=True, header_style="bold magenta")

    for header in headers:
        table.add_column(header)

    for schedule in schedules:
        qualifying_date = schedule.Qualifying.Date if schedule.Qualifying else "None"
        qualifying_time = schedule.Qualifying.Time if schedule.Qualifying else "None"
        sprint_date = schedule.Sprint.Date if schedule.Sprint else "None"
        sprint_time = schedule.Sprint.Time if schedule.Sprint else "None"

        data = (
            schedule.Round,
            schedule.RaceName,
            schedule.Date,
            schedule.Time if schedule.Time else "None",
            qualifying_date,
            qualifying_time,
            sprint_date,
            sprint_time,
        )

        table.add_row(*data)

    return table
