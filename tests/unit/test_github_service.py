"""
This will test some of the functionality of the GithubService class.

The GithubService class is responsible for interacting with the Github API.
"""
from datetime import datetime, timedelta

from src.api.github_service import GithubService


def test_should_update_should_return_true_if_last_checked_empty_string() -> None:
    """
    This will test the should_update method of the GithubService class.

    This will test if the method returns true if the last_checked parameter
    is an empty string.
    """
    github_service = GithubService({}, "")
    assert github_service.should_update() is True


def test_should_update_should_return_true_if_last_checked_a_number() -> None:
    """
    This will test the should_update method of the GithubService class.

    This will test if the method returns true if the last_checked config value
    is a number.
    """
    github_service = GithubService({"lastChecked": 100}, "")
    assert github_service.should_update() is True


def test_should_update_should_return_true_if_last_checked_more_than_a_day_ago() -> None:
    """
    This will test the should_update method of the GithubService class.

    This will test if the method returns true if the last_checked config value
    is more than a day ago.
    """
    yesterday = datetime.now() - timedelta(days=1)
    github_service = GithubService({"lastChecked": yesterday.isoformat()}, "")
    assert github_service.should_update() is True


def test_should_update_should_return_false_if_last_checked_an_hour_ago() -> None:
    """
    This will test the should_update method of the GithubService class.

    This will test if the method returns false if the last_checked config value
    is an hour ago.
    """
    yesterday = datetime.now() - timedelta(hours=1)
    github_service = GithubService({"lastChecked": yesterday.isoformat()}, "")
    assert github_service.should_update() is False


def test_process_release_data_should_return_new_release_patch():
    """
    This will test the process_release_data method of the GithubService class.

    This will test if the method returns a new release if the current release
    is older.
    """
    github_service = GithubService({"lastChecked": ""}, "1.0.0")

    release_data = [{"tag_name": "v1.0.0"}, {"tag_name": "v1.0.1"}]

    assert github_service.process_release_data(release_data) == {"tag_name": "v1.0.1"}


def test_process_release_data_should_return_none_patch():
    """
    This will test the process_release_data method of the GithubService class.

    This will test if the method returns None if the current release is the
    latest.
    """
    github_service = GithubService({"lastChecked": ""}, "1.0.1")

    release_data = [{"tag_name": "v1.0.0"}, {"tag_name": "v1.0.1"}]

    assert github_service.process_release_data(release_data) is None


def test_process_release_data_should_return_new_release_minor():
    """
    This will test the process_release_data method of the GithubService class.

    This will test if the method returns a new release if the current release
    is older.
    """
    github_service = GithubService({"lastChecked": ""}, "1.0.0")

    release_data = [{"tag_name": "v1.0.0"}, {"tag_name": "v1.1.0"}]

    assert github_service.process_release_data(release_data) == {"tag_name": "v1.1.0"}


def test_process_release_data_should_return_none_minor():
    """
    This will test the process_release_data method of the GithubService class.

    This will test if the method returns None if the current release is the
    latest.
    """
    github_service = GithubService({"lastChecked": ""}, "1.1.0")

    release_data = [{"tag_name": "v1.0.0"}, {"tag_name": "v1.1.0"}]

    assert github_service.process_release_data(release_data) is None


def test_process_release_data_should_return_new_release_major():
    """
    This will test the process_release_data method of the GithubService class.

    This will test if the method returns a new release if the current release
    is older.
    """
    github_service = GithubService({"lastChecked": ""}, "1.0.0")

    release_data = [{"tag_name": "v1.0.0"}, {"tag_name": "v2.0.0"}]

    assert github_service.process_release_data(release_data) == {"tag_name": "v2.0.0"}


def test_process_release_data_should_return_none_major():
    """
    This will test the process_release_data method of the GithubService class.

    This will test if the method returns None if the current release is the
    latest.
    """
    github_service = GithubService({"lastChecked": ""}, "2.0.0")

    release_data = [{"tag_name": "v1.0.0"}, {"tag_name": "v2.0.0"}]

    assert github_service.process_release_data(release_data) is None
