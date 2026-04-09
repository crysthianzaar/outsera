from unittest import TestCase

from app_factory import create_app
from tests.integration.conftest import TestConfig


class TestRichardsonMaturityLevel2(TestCase):
    def setUp(self):
        app = create_app(TestConfig())
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_get_returns_200(self):
        self.assertEqual(self.client.get("/producers/award-intervals").status_code, 200)

    def test_post_on_readonly_resource_returns_405(self):
        self.assertEqual(self.client.post("/producers/award-intervals").status_code, 405)

    def test_put_on_readonly_resource_returns_405(self):
        self.assertEqual(self.client.put("/producers/award-intervals").status_code, 405)

    def test_delete_on_readonly_resource_returns_405(self):
        self.assertEqual(self.client.delete("/producers/award-intervals").status_code, 405)

    def test_unknown_route_returns_404(self):
        self.assertEqual(self.client.get("/does-not-exist").status_code, 404)

    def test_404_response_is_json(self):
        response = self.client.get("/does-not-exist")
        self.assertEqual(response.content_type, "application/json")
        self.assertIn("error", response.json)

    def test_response_content_type_is_json(self):
        self.assertEqual(
            self.client.get("/producers/award-intervals").content_type,
            "application/json",
        )
