from unittest import TestCase

from app_factory import create_app
from tests.integration.conftest import TestConfig


class TestHealthEndpoints(TestCase):
    def setUp(self):
        app = create_app(TestConfig())
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_ping_returns_pong(self):
        response = self.client.get("/ping")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "pong")

    def test_health_returns_ok(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "ok")
