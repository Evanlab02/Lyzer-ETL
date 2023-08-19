"""
This module contains the load_app command line interface.

The load_app command line interface is responsible for loading data into the database.
"""


from threading import Thread
from typing_extensions import Annotated

from requests import HTTPError
from rich.console import Console
from typer import Typer, Option

from src.api.ergast_service import ErgastService
from src.database.mongo_service import MongoService
from src.helpers.utilities import validate_year, generate_schedules_table

load_app = Typer(pretty_exceptions_show_locals=False)
console = Console()
status = console.status("[bold green]Loading...")

ergast_service = ErgastService()
mongo_service = MongoService()


@load_app.command()
def schedule(year: Annotated[int, Option(prompt=True)]):
    """
    Load schedules into the database.

    Args:
        year (int): The year to load schedules for.
    """
    status.start()
    try:
        validate_year(year, allow_future=True)
        status.update("[bold green]Loading schedules from ergast...")
        schedules = ergast_service.get_schedules(year)
        status.update("[bold green]Inserting schedules into database...")
        thread = run_thread(mongo_service.insert_schedules, (year, schedules))
        table = generate_schedules_table(schedules)
        console.print(table)
        thread.join()
        status.stop()
    except Exception as error:
        handle_error(error)


def run_thread(func, args: tuple) -> Thread:
    """
    Run a thread.

    Args:
        func (function): The function to run.
        args (tuple): The arguments to pass to the function.

    Returns:
        Thread: The thread.
    """
    thread = Thread(target=func, args=args)
    thread.start()
    return thread


def handle_error(error: Exception):
    """
    Handle an error.

    Args:
        error (Exception): The error to handle.
    """
    status.stop()
    if isinstance(error, ValueError):
        console.print(f"[bold red]Value error: {error}")
    elif isinstance(error, HTTPError):
        console.print(f"[bold red]HTTP error: {error}")
    else:
        console.print(f"[bold red]Unexpected error: {error}")
