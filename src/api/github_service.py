"""
This module contains the GithubService class.

The GithubService class is responsible for all interactions with the Github API.
"""

from datetime import datetime

import requests
from rich import print as rich_print
from wget import download

from src.config.configuration import HOME_DIRECTORY, write_config
from src.error.exceptions import GithubRequestError

HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


class GithubService:
    """The GithubService class is responsible for all interactions with the Github API."""

    def __init__(self, config: dict, current_release: str):
        """Initialize the GithubService class."""
        self.config = config
        self.github_url = "https://api.github.com/repos/Evanlab02/Lyzer-ETL/releases"
        self.last_checked = config.get("lastChecked", "")
        self.current_release = current_release

    def update_app(self, force: bool = False):
        """Check for a new release on Github."""
        update_app = force if force else self.should_update()
        self.last_checked = datetime.now().isoformat()
        self.config["lastChecked"] = self.last_checked
        write_config(self.config)

        if update_app:
            release_data = self.get_latest_release_data()
            new_release = self.process_release_data(release_data)
            if new_release:
                self.download_release(new_release)

    def should_update(self):
        """Determine if the app should check for a new release."""
        if not self.last_checked or not isinstance(self.last_checked, str):
            return True

        if self.last_checked:
            last_checked_date = datetime.fromisoformat(self.last_checked)
            days_since_last_check = (datetime.now() - last_checked_date).days
            if days_since_last_check >= 1:
                return True

        return False

    def get_latest_release_data(self):
        """Get the latest release from Github."""
        rich_print("Checking for updates...")
        response = requests.get(self.github_url, headers=HEADERS, timeout=30)
        if response.status_code == 200:
            return response.json()
        elif response.status_code != 404:
            raise GithubRequestError(response.status_code)

    def process_release_data(self, release_data: dict):
        """Process the release data from Github."""
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

    def download_release(self, release: dict):
        """Download the latest release from Github."""
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
