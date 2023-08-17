"""
The load_cli module contains the load command for the CLI.

This module contains the load command for the CLI. This command will load data
from the Ergast API into the MongoDB database based on the subcommand that is
called.
"""

from threading import Thread
from typer import Typer, Option
from typing_extensions import Annotated

from rich import print as rich_print
from rich.console import Console

from src.api.ergast_service import ErgastService
from src.config.configuration import read_config
from src.database.mongo_service import MongoService
from src.error.exceptions import ErgastRequestError
from src.helpers.utilities import validate_year, generate_table
from src.services.transformation_service import TransformationService

load_app = Typer(pretty_exceptions_show_locals=False)

CONSOLE = Console()
CONFIG = read_config()
MONGO_URI = CONFIG["mongoUri"]

ERGAST_SERVICE = ErgastService()
FORMATION_SERVICE = TransformationService()
MONGO_SERVICE = MongoService(MONGO_URI)


@load_app.command()
def schedule(year: Annotated[int, Option(prompt=True)]):
    """
    Load the schedule data from the Ergast API into the MongoDB database.

    This command will load the schedule data from the Ergast API into the
    MongoDB database. The data will be loaded into the Schedules database
    and will be stored in the collection for the specified year.

    Args:
        year (int): The year to load the schedule data for.
    """
    try:
        year = validate_year(year, allow_future=True)
        response = ERGAST_SERVICE.get_schedule_data(year)
        schedules = FORMATION_SERVICE.transform_schedule(response)
        thread = load_data("Schedules", year, schedules)
        CONSOLE.print(generate_table(schedules))
        thread.join()
    except Exception as error:
        handle_error(error)


def load_data(database: str, collection: str, data: list[dict]):
    """
    Load data into the MongoDB database.

    This function will load the data into the MongoDB database. It will
    create a new thread to do this so that the CLI can continue to run
    while the data is being loaded.

    Args:
        database (str): The database to load the data into.
        collection (str): The collection to load the data into.
        data (list[dict]): The data to load into the database.

    Returns:
        Thread: The thread that is loading the data into the database.
    """
    mongo_thread = Thread(
        target=MONGO_SERVICE.insert_many, args=(str(database), str(collection), data)
    )
    mongo_thread.start()
    return mongo_thread


def handle_error(error: Exception):
    """
    Handle an error.

    This function will handle errors that occur when using the CLI. It will
    print out the error message to the console.

    Args:
        error (Exception): The error that occurred.
    """
    if isinstance(error, ValueError):
        rich_print(f"[red]ValueError[/red]: {error}")
    elif isinstance(error, ErgastRequestError):
        rich_print(f"[red]ErgastRequestError[/red]: {error.status_code}")
    else:
        rich_print(f"[red]Error[/red]: {error}")
