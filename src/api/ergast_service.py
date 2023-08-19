"""
This module contains the ErgastService class.

The ErgastService class is responsible for all interactions with the Ergast API.
"""

import requests

from src.models.schedules import ScheduleResponse, Schedule


class ErgastService:
    """
    This class is responsible for all interactions with the Ergast API.

    Attributes:
        base_url (str): The base url for the Ergast API.

    Methods:
        get_data: Get data from the Ergast API.
        get_schedules: Get schedules from the Ergast API.
    """

    def __init__(self) -> None:
        """Construct the ErgastService class."""
        self.base_url = "https://ergast.com/api/f1"

    def get_data(self, url: str) -> dict | list[dict]:
        """
        Get data from the Ergast API.

        Args:
            url (str): The url to get data from.

        Returns:
            dict | list[dict]: The data from the Ergast API.

        Raises:
            HTTPError: If the response status code is not ok.
        """
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_schedules(self, year: int) -> list[Schedule]:
        """
        Get schedules from the Ergast API.

        Args:
            year (int): The year to get schedules for.

        Returns:
            list[dict]: The schedules from the Ergast API.

        Raises:
            HTTPError: If the response status code is not ok.
        """
        url = f"{self.base_url}/{year}.json"
        data = self.get_data(url)
        response = ScheduleResponse(**data)
        return response.MRData.RaceTable.Races
