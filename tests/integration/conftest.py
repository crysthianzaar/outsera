import os

import pytest

from config import Config
from create_app import create_app


class AppConfig(Config):
    DATABASE_URL: str = "sqlite:///:memory:"
    CSV_PATH: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../infra/data/movielist.csv"))
    IN_MEMORY_DB: bool = True


@pytest.fixture()
def client():
    app = create_app(AppConfig())
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c
