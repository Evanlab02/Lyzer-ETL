"""This module contains the configuration functions for the Lyzer-ETL application."""

import json
import os
from os import path

from src.database.mongo_service import MongoService

HOME_DIRECTORY = path.expanduser("~")
CONFIG_DIRECTORY = path.join(HOME_DIRECTORY, ".lyzer")
CONFIG_FILE = path.join(CONFIG_DIRECTORY, "config.json")


def setup_app():
    """
    Configure the Lyzer-ETL application.

    This function will setup the application, ensuring all required values
    are present in the configuration file.
    """
    if not (os.path.exists(CONFIG_FILE)):
        create_config()


def create_config():
    """Create the config to be used by the whole application."""
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


def read_config():
    """
    Read the config file.

    Returns:
        dict: the config file as a dictionary
    """
    with open(CONFIG_FILE, "r", encoding="UTF-8") as config:
        return json.load(config)


def write_config(config: dict):
    """
    Write the config file.

    Args:
        config (dict): the config file as a dictionary
    """
    with open(CONFIG_FILE, "w+", encoding="UTF-8") as config_file:
        json.dump(config, config_file, indent=4)
