from src.database.mongo_service import MongoService


def test_connection_should_return_true() -> None:
    """
    Test the test_connection function.
    """
    mongo_service = MongoService()
    assert mongo_service.test_connection("mongodb://localhost:27017/") is True


def test_connection_should_return_false() -> None:
    """
    Test the test_connection function.
    """
    mongo_service = MongoService()
    assert mongo_service.test_connection("") is False
