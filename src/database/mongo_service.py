"""
This module contains the MongoService class.

The MongoService class is responsible for all interactions with the MongoDB database.
"""

from pymongo import MongoClient


class MongoService:
    """
    This class is responsible for all interactions with the MongoDB database.

    Attributes:
        client (MongoClient): The MongoDB client.
        db (Database): The MongoDB database.
        collection (Collection): The MongoDB collection.

    Methods:
        hello_world: Prints "Hello, world!" to the console.
        goodbye_world: Prints "Goodbye, world!" to the console.
    """

    def __init__(self) -> None:
        """Construct the MongoService class."""
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["test"]
        self.collection = self.db["test"]

    def hello_world(self):
        """Print "Hello, world!" to the console."""
        print("Hello, world!")

    def goodbye_world(self):
        """Print "Goodbye, world!" to the console."""
        print("Goodbye, world!")
