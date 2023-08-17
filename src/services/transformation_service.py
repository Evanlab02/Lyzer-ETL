"""
This file contains the TransformationService class.

The TransformationService class is responsible for transforming the data from the Ergast API
into the format that is required for the MongoDB database.
"""

from rich.console import Console

from src.models.schedules import Schedule


class TransformationService:
    """
    Transform the data from the Ergast API into the format that is required for Database.

    This class is used to transform the data from the Ergast API into the format that is
    required for the MongoDB database.

    Attributes:
        console (Console): The rich console.
    """

    def __init__(self) -> None:
        """
        Construct the TransformationService class.

        The rich console is used to display status messages to the user.
        """
        self.console = Console()

    def transform_schedule(self, ergast_response):
        """
        Transform the schedule data from the Ergast API into the format that is required.

        This function will transform the schedule data from the Ergast API into the format
        that is required for the MongoDB database.

        Args:
            ergast_response (dict): The response from the Ergast API.

        Returns:
            list[dict]: The transformed schedule data.
        """
        with self.console.status(status="[bold green]Transforming data..."):
            data = ergast_response["MRData"]["RaceTable"]["Races"]
            schedules = [Schedule(**schedule) for schedule in data]
            return [schedule.model_dump() for schedule in schedules]
