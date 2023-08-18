"""
The parent folder for all modules.

All Lyzer-ETL source code is contained within this folder.
"""

# Local imports

from os import environ

from src.config.configuration import read_config
from src.config.configuration import setup_app

setup_app()
config = read_config()
environ["mongoUri"] = config["mongoUri"]
