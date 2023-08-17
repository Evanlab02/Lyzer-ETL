"""
This module contains the MongoService class.

The MongoService class is responsible for all interactions with the MongoDB database.
"""

from pymongo import MongoClient
from rich import print as rich_print


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
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["test"]
        self.collection = self.db["test"]

    def test_connection(self, connection_uri: str) -> bool:
        """
        Tests validity of connection uri given by user.

        Args:
            connection_string (str): Mongo uri given by user.

        Returns:
            bool: True if valid connection string.
        """
        try:
            client = MongoClient(connection_uri)
            client.admin.command("ping")
            rich_print("[green]Ping successful.[/green]")
            rich_print("[green]Connection string entered is valid.[/green]")
        except Exception as error:
            rich_print("[red]Ping unsuccessful.[/red]")
            rich_print("[red]Connection string entered is invalid.[/red]")
            rich_print(f"\n[red]Error: {error}[/red]\n")
            rich_print("[red]Please try again.[/red]")
            return False

        return True
