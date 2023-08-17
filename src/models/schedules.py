"""
This file contains the schedule model for the application.

The schedule model is used by the transformation service to transform the data from the
Ergast API into the format that is required for the MongoDB database.
"""

from pydantic import BaseModel, Field
from typing import Optional


class Session(BaseModel):
    """
    This class is used to represent a session in the schedule model.

    Attributes:
        Date (Optional[str]): The date of the session.
        Time (Optional[str]): The time of the session.
    """

    Date: Optional[str] = Field(alias="date")
    Time: Optional[str] = Field(alias="time")


class Schedule(BaseModel):
    """
    This class is used to represent a schedule item.

    Attributes:
        Round (int): The round.
        RaceName (str): The race name.
        Date (str): The date.
        Time (Optional[str]): The time.
        FirstPractice (Optional[Session]): The first practice session.
        SecondPractice (Optional[Session]): The second practice session.
        ThirdPractice (Optional[Session]): The third practice session.
        Qualifying (Optional[Session]): The qualifying session.
        Sprint (Optional[Session]): The sprint session.
    """

    Round: int = Field(alias="round")
    RaceName: str = Field(alias="raceName")
    Date: str = Field(alias="date")
    Time: str = Field(alias="time", default=None)
    FirstPractice: Optional[Session] = None
    SecondPractice: Optional[Session] = None
    ThirdPractice: Optional[Session] = None
    Qualifying: Optional[Session] = None
    Sprint: Optional[Session] = None
