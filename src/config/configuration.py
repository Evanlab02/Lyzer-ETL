"""
This module contains the configuration functions for the Lyzer-ETL application.

Functions:
    setup_app: Configure the Lyzer-ETL application.
    create_config: Create the config to be used by the whole application.
    read_config: Read the config file.
    write_config: Write the config file.
"""

# Standard Library Imports
import json
import os
from datetime import datetime
from rich import print as rich_print

# Local Imports
from src.database.mongo_service import MongoService

# Constants
HOME_DIRECTORY = os.path.expanduser("~")
CONFIG_DIRECTORY = os.path.join(HOME_DIRECTORY, ".lyzer")
CONFIG_FILE = os.path.join(CONFIG_DIRECTORY, "config.json")


def setup_app() -> None:
    """
    Configure the Lyzer-ETL application.

    This function will setup the application, ensuring all required values
    are present in the configuration file.
    """
    if not (os.path.exists(CONFIG_FILE)):
        rich_print("[blue]Setting up config[/blue]")
        create_config()


def create_config() -> None:
    """
    Create the config to be used by the whole application.

    This function will create the config file and ask the user for the mongo connection string.
    """
    if not (os.path.exists(CONFIG_DIRECTORY)):
        os.makedirs(CONFIG_DIRECTORY)

    config = get_connection_string()

    config.update({"lastUpdated": ""})

    write_config(config=config)


def read_config() -> dict | list:
    """
    Read the config file.

    Returns:
        dict | list: the config file as a dictionary.
    """
    with open(CONFIG_FILE, "r", encoding="UTF-8") as config:
        return json.load(config)


def write_config(config: dict | list) -> None:
    """
    Write the config file.

    Args:
        config (dict | list): the config file as a dictionary.
    """
    with open(CONFIG_FILE, "w+", encoding="UTF-8") as config_file:
        rich_print("\n[blue]Updating config file...[/blue]")
        config["lastUpdated"] = str(datetime.now())
        json.dump(config, config_file, indent=4)
        rich_print("\n[green]Config file updated[/green]")


def get_connection_string(config: dict | list = {}) -> dict | list:
    """Get the mongo connection string from user.

    Args:
        config (dict | list, optional): Config to update or write to. Defaults to {}.

    Returns:
        dict | list: Updated config or new config populated with Mongo URI
    """
    valid = False

    while not valid:
        connection_uri = input("\nEnter your mongo connection string: ")
        os.environ["mongoUri"] = connection_uri
        valid = MongoService().test_connection(connection_uri)

    if len(config.keys()) == 0:
        config.update({"mongoUri": connection_uri})
    else:
        config["mongoUri"] = connection_uri

    return config
