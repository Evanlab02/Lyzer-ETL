"""
This module contains the MongoService class.

The MongoService class is responsible for all interactions with the MongoDB database.
"""

from os import environ

from pymongo import MongoClient
from rich import print as rich_print
from rich.console import Console

from src.models.schedules import Schedule


class MongoService:
    """
    This class is responsible for all interactions with the MongoDB database.

    Attributes:
        client (MongoClient): The MongoDB client.
        db (Database): The MongoDB database.
        collection (Collection): The MongoDB collection.

    Methods:
        test_connection: Test the validity of the connection string given by the user.
    """

    def __init__(self) -> None:
        """
        Construct the MongoService class.

        This will create the MongoDB client, database, and collection.
        """
        connection_string = environ["mongoUri"]
        self.console = Console()
        self.client = MongoClient(connection_string)

    def test_connection(self, connection_uri: str) -> bool:
        """
        Tests validity of connection uri given by user.

        Args:
            connection_string (str): Mongo uri given by user.

        Returns:
            bool: True if valid connection string.
        """
        status = self.console.status("[bold green]Testing connection...")
        status.start()
        try:
            client = MongoClient(connection_uri)
            client.admin.command("ping")
            status.stop()
            rich_print("[green]Ping successful.[/green]")
            rich_print("[green]Connection string entered is valid.[/green]")
        except Exception as error:
            status.stop()
            rich_print("[red]Ping unsuccessful.[/red]")
            rich_print("[red]Connection string entered is invalid.[/red]")
            rich_print(f"\n[red]Error: {error}[/red]\n")
            rich_print("[red]Please try again.[/red]")
            return False

        return True

    def insert_schedules(self, year: int, schedules: list[Schedule]):
        """
        Insert schedules into the database.

        Args:
            year (int): The year to insert schedules for.
            schedules (list[Schedule]): The schedules to insert.

        Returns:
            None
        """
        database = self.client["Schedules"]
        collection = database[str(year)]
        collection.drop()
        schedules = [schedule.model_dump() for schedule in schedules]
        collection.insert_many(schedules)
