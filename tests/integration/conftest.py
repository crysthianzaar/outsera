import os
import pytest

from app_factory import create_app
from config import Config


class TestConfig(Config):
    DATABASE_URL = "sqlite:///:memory:"
    CSV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/movielist.csv"))
    API_TOKEN = None


class TestConfigWithToken(TestConfig):
    API_TOKEN = "test-secret-token"


@pytest.fixture()
def client():
    app = create_app(TestConfig())
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


@pytest.fixture()
def client_with_token():
    app = create_app(TestConfigWithToken())
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c
