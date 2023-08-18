"""
Contains schedule and related models.

Classes:
    Session: A session.
    Schedule: A schedule.
    ScheduleTable: A schedule table.
    MasterData: Master data.
    ScheduleResponse: A schedule response.
"""
from typing import Optional

from pydantic import BaseModel, Field


class Session(BaseModel):
    """
    Session model.

    Attributes:
        Date (str): The date of the session.
        Time (str): The time of the session.
    """

    Date: Optional[str] = Field(alias="date", default=None)
    Time: Optional[str] = Field(alias="time", default=None)


class Schedule(BaseModel):
    """
    Schedule model.

    Attributes:
        Round (int): The round of the schedule.
        RaceName(str): The race name.
        Date (str): The date of the race.
        Time (str): The time of the race.
        FirstPractice (Session): The first practice session.
        SecondPractice (Session): The second practice session.
        ThirdPractice (Session): The third practice session.
        Qualifying (Session): The qualifying session.
        Sprint (Session): The sprint session.
    """

    Round: int = Field(alias="round")
    RaceName: str = Field(alias="raceName")
    Date: str = Field(alias="date")
    Time: Optional[str] = Field(alias="time", default=None)
    FirstPractice: Optional[Session] = Field(alias="FirstPractice", default=None)
    SecondPractice: Optional[Session] = Field(alias="SecondPractice", default=None)
    ThirdPractice: Optional[Session] = Field(alias="ThirdPractice", default=None)
    Qualifying: Optional[Session] = Field(alias="Qualifying", default=None)
    Sprint: Optional[Session] = Field(alias="Sprint", default=None)


class ScheduleTable(BaseModel):
    """
    Schedule table model.

    Attributes:
        Races (list[Schedule]): List of schedules for events.
    """

    Races: list[Schedule] = Field(alias="Races")


class MasterData(BaseModel):
    """
    Master data model.

    Attributes:
        RaceTable (ScheduleTable): The schedule table.
    """

    RaceTable: ScheduleTable = Field(alias="RaceTable")


class ScheduleResponse(BaseModel):
    """
    Schedule response model.

    Attributes:
        MRData (MasterData): The master data object.
    """

    MRData: MasterData = Field(alias="MRData")
