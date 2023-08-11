"""Contains all custom exceptions for the project."""


class GithubRequestError(Exception):
    """Raised when a request to the Github API fails."""

    def __init__(self, status_code: int, *args: object) -> None:
        """Construct the GithubRequestError class."""
        self.status_code = status_code
        super().__init__(*args)
