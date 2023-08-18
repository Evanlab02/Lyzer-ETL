"""
Contains integration tests for the MongoService class.
"""
import pymongo

from src.database.mongo_service import MongoService
from src.models.schedules import Schedule


def test_connection_should_return_true() -> None:
    """
    Test the test_connection function.
    """
    mongo_service = MongoService()
    assert mongo_service.test_connection("mongodb://localhost:27017/") is True


def test_connection_should_return_false() -> None:
    """
    Test the test_connection function.
    """
    mongo_service = MongoService()
    assert mongo_service.test_connection("") is False


def test_insert_schedule_works_correctly() -> None:
    """
    Test the insert_schedule function.
    """
    mongo_service = MongoService()
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    mongo_service.client = client

    schedules = [
        Schedule(
            round=1, raceName="Bahrain Grand Prix", date="2021-03-28", time="15:00:00Z"
        ),
        Schedule(
            round=2,
            raceName="Emilia Romagna Grand Prix",
            date="2021-04-18",
            time="13:00:00Z",
        ),
    ]

    mongo_service.insert_schedules(2021, schedules)

    db = client["Schedules"]
    collection = db["2021"]
    assert collection.count_documents({}) == 2
    assert collection.find_one({"Round": 1})["RaceName"] == "Bahrain Grand Prix"
    assert collection.find_one({"Round": 2})["RaceName"] == "Emilia Romagna Grand Prix"
    collection.drop()
