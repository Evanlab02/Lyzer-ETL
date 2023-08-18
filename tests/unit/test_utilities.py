"""Contains tests for the utility functions."""
from datetime import datetime

import pytest

from src.helpers.utilities import validate_year


def test_validate_year_with_year_before_1950():
    """
    Test the validate_year function with a year before 1950.
    """
    with pytest.raises(ValueError):
        validate_year(1949)


def test_validate_year_with_year_after_current():
    """
    Test the validate_year function with a year after current.
    """
    current_year = datetime.now().year
    future_year = current_year + 1
    with pytest.raises(ValueError):
        validate_year(future_year)


def test_validate_year_with_year_2_years_after_current():
    """
    Test the validate_year function with a year 2 years after current.
    """
    current_year = datetime.now().year
    future_year = current_year + 2
    with pytest.raises(ValueError):
        validate_year(future_year, allow_future=True)
