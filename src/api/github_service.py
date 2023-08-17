"""
This module contains the GithubService class.

The GithubService class is responsible for all interactions with the Github API.
"""

# System imports
import sys
from datetime import datetime

# Third-party imports
import requests
from rich import print as rich_print
from wget import download

# Local imports
from src.config.configuration import HOME_DIRECTORY, write_config
from src.error.exceptions import GithubRequestError

# Constants
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


class GithubService:
    """
    The GithubService class is responsible for all interactions with the Github API.

    Attributes:
        config (dict): The configuration data for the application.
        github_url (str): The URL for the Github API.
        last_checked (str): The date and time the application last checked for an update.
        current_release (str): The current release of the application.

    Methods:
        update_app: Check for a new release on Github, and if one is available, download it.
        should_update: Determine if the app should check for a new release.
        get_release_data: Get all the releases data from Github.
        process_release_data: Process the release data from Github to find the latest release.
        download_release: Download the given release from Github.
    """

    def __init__(self, config: dict, current_release: str) -> None:
        """
        Initialize the GithubService class.

        Args:
            config (dict): The configuration data for the application.
            current_release (str): The current release of the application.
        """
        self.config = config
        self.github_url = "https://api.github.com/repos/Evanlab02/Lyzer-ETL/releases"
        self.last_checked = config.get("lastChecked", "")
        self.current_release = current_release

    def update_app(self, force: bool = False) -> None:
        """
        Check for a new release on Github, and if one is available, download it.

        This will check the config file to see when last there was a check for a new update.
        If it has been more than a day since the last check, it will check Github for a new
        release. If there is a new release, it will download it.

        Args:
            force (bool): Force the application to check for a new release regardless
                of when the last check was.
        """
        update_app = force if force else self.should_update()
        self.last_checked = datetime.now().isoformat()
        self.config["lastChecked"] = self.last_checked
        write_config(self.config)

        if update_app:
            release_data = self.get_release_data()
            new_release = self.process_release_data(release_data)
            if new_release:
                self.download_release(new_release)

    def should_update(self) -> bool:
        """
        Determine if the app should check for a new release.

        This will check the config file to see when last there was a check for a new update.
        If it has been more than a day since the last check, it will return True. Otherwise,
        it will return False.

        Returns:
            bool: True if the app should check for a new release, False otherwise.
        """
        if not self.last_checked or not isinstance(self.last_checked, str):
            return True

        if self.last_checked:
            last_checked_date = datetime.fromisoformat(self.last_checked)
            days_since_last_check = (datetime.now() - last_checked_date).days
            if days_since_last_check >= 1:
                return True

        return False

    def get_release_data(self) -> list[dict]:
        """
        Get the latest release from Github.

        Returns:
            list[dict]: The JSON data from Github.

        Raises:
            GithubRequestError: If the request to Github fails.
        """
        rich_print("Checking for updates...")
        response = requests.get(self.github_url, headers=HEADERS, timeout=30)
        if response.status_code == 200:
            return response.json()
        elif response.status_code != 200:
            raise GithubRequestError(response.status_code)

    def process_release_data(self, release_data: list[dict]) -> dict | None:
        """
        Process the release data from Github.

        This will process the release data from Github to find the latest release.

        Args:
            release_data (list[dict]): The JSON data from Github.

        Returns:
            dict: The latest release data from Github.

        Raises:
            GithubRequestError: If the request to Github fails.
        """
        for release in release_data:
            is_new_release = False

            tag_name = release.get("tag_name", "")
            tag_name = tag_name.replace("v", "")
            tag_major = int(tag_name.split(".")[0])
            tag_minor = int(tag_name.split(".")[1])
            tag_patch = int(tag_name.split(".")[2])

            current_major = int(self.current_release.split(".")[0])
            current_minor = int(self.current_release.split(".")[1])
            current_patch = int(self.current_release.split(".")[2])

            if tag_major > current_major:
                is_new_release = True
            elif tag_major == current_major and tag_minor > current_minor:
                is_new_release = True
            elif (
                tag_major == current_major
                and tag_minor == current_minor
                and tag_patch > current_patch
            ):
                is_new_release = True

            if is_new_release:
                return release

    def download_release(self, release: dict) -> None:
        """
        Download the latest release from Github.

        This will download the latest release from Github and save it to the
        user's home directory.

        Args:
            release (dict): The latest release data from Github.
        """
        rich_print(f"Found new release: {release.get('tag_name')}")

        confirm_update = input(
            "A new release is available. Would you like to update? (y/N): "
        )

        if confirm_update.casefold() == "y":
            assets = release.get("assets", [])
            asset_data = [
                {
                    "name": asset.get("name", ""),
                    "url": asset.get("browser_download_url", ""),
                }
                for asset in assets
            ]

            download_asset_directory = f"{HOME_DIRECTORY}/Lyzer-ETL"

            for asset in asset_data:
                if asset["name"] == "Lyzer-ETL":
                    download(asset["url"], out=download_asset_directory)
                    break

            rich_print(f"\nFind updated file at '{download_asset_directory}'.")
            rich_print("Please overwrite your existing executable.")
            rich_print("[green]Update Complete.[/green]")
            sys.exit(0)
