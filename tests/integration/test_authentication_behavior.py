from unittest import TestCase

from app_factory import create_app
from tests.integration.conftest import TestConfig, TestConfigWithToken


class TestAuthenticationBehavior(TestCase):
    def setUp(self):
        open_app = create_app(TestConfig())
        open_app.config["TESTING"] = True
        self.open_client = open_app.test_client()

        secured_app = create_app(TestConfigWithToken())
        secured_app.config["TESTING"] = True
        self.secured_client = secured_app.test_client()

    def test_endpoint_is_open_without_token_configured(self):
        self.assertEqual(self.open_client.get("/producers/award-intervals").status_code, 200)

    def test_endpoint_requires_token_when_configured(self):
        self.assertEqual(self.secured_client.get("/producers/award-intervals").status_code, 401)

    def test_endpoint_accepts_valid_token(self):
        response = self.secured_client.get(
            "/producers/award-intervals",
            headers={"Authorization": "Bearer test-secret-token"},
        )
        self.assertEqual(response.status_code, 200)

    def test_endpoint_rejects_invalid_token(self):
        response = self.secured_client.get(
            "/producers/award-intervals",
            headers={"Authorization": "Bearer wrong-token"},
        )
        self.assertEqual(response.status_code, 401)
