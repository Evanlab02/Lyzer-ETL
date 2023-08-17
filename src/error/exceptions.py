"""
Contains all custom exceptions for the project.

Classes:
    GithubRequestError: Raised when a request to the Github API fails.
"""


class GithubRequestError(Exception):
    """
    Raised when a request to the Github API fails.

    Attributes:
        status_code (int): The status code of the response.
    """

    def __init__(self, status_code: int, *args: object) -> None:
        """Construct the GithubRequestError class."""
        self.status_code = status_code
        super().__init__(*args)


class ErgastRequestError(Exception):
    """
    Raised when a request to the Ergast API fails.

    Attributes:
        status_code (int): The status code of the response.
    """

    def __init__(self, status_code: int, *args: object) -> None:
        """Construct the ErgastRequestError class."""
        self.status_code = status_code
        super().__init__(*args)
