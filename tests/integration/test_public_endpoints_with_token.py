from unittest import TestCase

from app_factory import create_app
from tests.integration.conftest import TestConfigWithToken


class TestPublicEndpointsWithTokenConfigured(TestCase):
    def setUp(self):
        app = create_app(TestConfigWithToken())
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_ping_is_public_even_with_token(self):
        self.assertEqual(self.client.get("/ping").status_code, 200)

    def test_health_is_public_even_with_token(self):
        self.assertEqual(self.client.get("/health").status_code, 200)
