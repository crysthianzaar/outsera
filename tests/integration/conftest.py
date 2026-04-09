import pytest

from create_app import create_app
from tests.integration.test_config import AppConfig


@pytest.fixture()
def client():
    app = create_app(AppConfig())
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c
