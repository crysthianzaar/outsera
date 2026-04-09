from unittest import TestCase

from create_app import create_app
from tests.integration.test_config import AppConfig as TestConfig


class TestHealthEndpoints(TestCase):
    @classmethod
    def setUpClass(cls):
        app = create_app(TestConfig())
        app.config["TESTING"] = True
        cls.client = app.test_client()

    def test_ping_returns_pong(self):
        response = self.client.get("/ping")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "pong")

    def test_health_returns_ok(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "ok")
