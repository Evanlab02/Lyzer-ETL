"""
This module contains the ErgastService class.

The ErgastService class is responsible for all interactions with the Ergast API.
"""

import requests

from rich.console import Console

from src.error.exceptions import ErgastRequestError


class ErgastService:
    """
    This class is responsible for all interactions with the Ergast API.

    Attributes:
        console (Console): The rich Console class.
        base_url (str): The base URL for the Ergast API.

    Methods:
        handle_response: Handle the response from the Ergast API.
        get_schedule_data: Get the schedule data from the Ergast API.
    """

    def __init__(self):
        """
        Construct the ErgastService class.

        This will create the rich Console class and set the base URL for the Ergast API.
        """
        self.console = Console()
        self.base_url = "http://ergast.com/api/f1"

    def handle_response(self, response: requests.Response) -> list | dict:
        """
        Handle the response from the Ergast API.

        Args:
            response (requests.Response): The response from the Ergast API.

        Returns:
            list | dict: The JSON response from the Ergast API.

        Raises:
            ErgastRequestError: Raised when the response status code is not 200.
        """
        if response.status_code != 200:
            raise ErgastRequestError(response.status_code)
        return response.json()

    def get_schedule_data(self, year: int):
        """
        Get the schedule data from the Ergast API.

        Args:
            year (int): The year to get the schedule data for.

        Returns:
            list | dict: The JSON response from the Ergast API.

        Raises:
            ErgastRequestError: Raised when the response status code is not 200.
        """
        with self.console.status(
            status="[bold green]Extracting schedules from Ergast..."
        ):
            response = requests.get(url=f"{self.base_url}/{year}.json", timeout=5)

            return self.handle_response(response)
