"""
This module contains the MongoService class.

The MongoService class is responsible for all interactions with the MongoDB database.
"""

from pymongo import MongoClient
from rich import print as rich_print
from rich.console import Console


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

    def __init__(self, connection_string: str) -> None:
        """
        Construct the MongoService class.

        This will create the rich Console class and the MongoDB client.

        Args:
            connection_string (str): The connection string for the MongoDB database.
        """
        self.console = Console()
        self.client = MongoClient(connection_string)

    def test_connection(self: str) -> bool:
        """
        Tests validity of connection uri given by user.

        Args:
            connection_string (str): Mongo uri given by user.

        Returns:
            bool: True if valid connection string.
        """
        with self.console.status(status="[bold green]Testing connection..."):
            try:
                self.client.admin.command("ping")
            except Exception:
                return False

            return True

    def insert_many(self, database: str, collection: str, data: list) -> bool:
        """
        Insert many documents into the MongoDB database.

        Args:
            database (str): The database to insert the data into.
            collection (str): The collection to insert the data into.
            data (list): The data to insert into the database.

        Returns:
            bool: True if the data was successfully inserted into the database.
        """
        if len(data) == 0:
            rich_print("[yellow]No data to load.[/yellow]")
            return False

        acknowledged = False
        with self.console.status(status="[bold green]Loading data into mongo..."):
            db = self.client[database]
            coll = db[collection]
            coll.drop()
            result = coll.insert_many(data)
            acknowledged = result.acknowledged

        if acknowledged:
            rich_print("[green]Data successfully loaded into mongo.[/green]")
        else:
            rich_print("[red]Data failed to load into mongo.[/red]")

        return acknowledged
