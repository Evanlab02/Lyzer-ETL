"""This module contains the configuration functions for the Lyzer-ETL application."""
import os
import json
from database.mongo_service import MongoService

def setup_app():
    """
    Configure the Lyzer-ETL application.

    This function will setup the application, ensuring all required values
    are present in the configuration file.
    """
    print("Hello, setup!")
    config_dir:str = os.getcwd() + "/src/.lyzer/config.json"
    
    if not (os.path.exists(config_dir)):
        create_config(config_dir)

def create_config(config_dir:str):
    """Creates the config to be used by the whole app

    Args:
        config_dir (str): directory of the config to be created
    """
    os.mkdir(config_dir)
    
    config_file = config_dir + "/config.json"
    config = {}

    valid = False
    while not valid:
        connection_uri = input("Enter your mongo connection string: ")
        valid = MongoService().test_connection(connection_uri)

    config.update({"mongoUri": connection_uri})
    with open(config_file, "w+") as c:
        c.write(json.dumps(config))


