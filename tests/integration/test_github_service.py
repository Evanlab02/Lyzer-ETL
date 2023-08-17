"""
Tests for the github_service module.

The github_service module is responsible for communicating with the GitHub API.
"""
# Third-party imports
import pytest

# Local imports
from src.api.github_service import GithubService
from src.error.exceptions import GithubRequestError


def test_get_release_data() -> None:
    """
    Test the get_release_data function.
    """
    github_service = GithubService({}, "")
    release_data = github_service.get_release_data()

    assert isinstance(release_data, list)
    assert len(release_data) > 0
    assert isinstance(release_data[0], dict)
    assert "tag_name" in release_data[0]


def test_get_release_data_invalid_repo() -> None:
    """
    Test the get_release_data function with an invalid repo.
    """
    github_service = GithubService({}, "")
    github_service.github_url = (
        "https://api.github.com/repos/Evanlab02/random-why-would-i-do-this/releases"
    )

    with pytest.raises(GithubRequestError):
        github_service.get_release_data()
