"""Contains tests for the ErgastService class."""

import pytest

from requests import HTTPError

from src.api.ergast_service import ErgastService
from src.models.schedules import Session


def test_get_schedules():
    """
    Test the get_schedules function.
    """
    ergast_service = ErgastService()
    schedules = ergast_service.get_schedules(2021)
    assert len(schedules) == 22
    assert isinstance(schedules[0].Round, int) is True
    assert isinstance(schedules[0].Date, str) is True
    assert isinstance(schedules[0].Time, str) is True
    assert isinstance(schedules[0].FirstPractice, Session) is True
    assert isinstance(schedules[0].SecondPractice, Session) is True
    assert isinstance(schedules[0].ThirdPractice, Session) is True
    assert isinstance(schedules[0].Qualifying, Session) is True


def test_invalid_endpoint():
    """
    Test the get_data function with an invalid endpoint.
    """
    ergast_service = ErgastService()
    with pytest.raises(HTTPError):
        ergast_service.get_data("https://ergast.com/api/f1/flowers/invalid.json")
