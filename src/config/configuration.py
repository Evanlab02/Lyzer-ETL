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
from os import path

# Local Imports
from src.database.mongo_service import MongoService

# Constants
HOME_DIRECTORY = path.expanduser("~")
CONFIG_DIRECTORY = path.join(HOME_DIRECTORY, ".lyzer")
CONFIG_FILE = path.join(CONFIG_DIRECTORY, "config.json")


def setup_app() -> None:
    """
    Configure the Lyzer-ETL application.

    This function will setup the application, ensuring all required values
    are present in the configuration file.
    """
    if not (os.path.exists(CONFIG_FILE)):
        create_config()


def create_config() -> None:
    """
    Create the config to be used by the whole application.

    This function will create the config file and ask the user for the mongo connection string.
    """
    os.makedirs(CONFIG_DIRECTORY)
    config = {}

    valid = False
    while not valid:
        connection_uri = input("Enter your mongo connection string: ")
        valid = MongoService().test_connection(connection_uri)

    config.update({"mongoUri": connection_uri})
    config.update({"lastChecked": ""})

    with open(CONFIG_FILE, "w+") as config_file:
        json.dump(config, config_file, indent=4)


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
        json.dump(config, config_file, indent=4)
