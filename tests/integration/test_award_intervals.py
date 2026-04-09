from unittest import TestCase

from create_app import create_app
from tests.integration.conftest import AppConfig as TestConfig


EXPECTED_MIN = [
    {
        "producer": "Joel Silver",
        "interval": 1,
        "previousWin": 1990,
        "followingWin": 1991,
    }
]

EXPECTED_MAX = [
    {
        "producer": "Matthew Vaughn",
        "interval": 13,
        "previousWin": 2002,
        "followingWin": 2015,
    }
]


class TestAwardIntervalsEndpoint(TestCase):
    @classmethod
    def setUpClass(cls):
        app = create_app(TestConfig())
        app.config["TESTING"] = True
        cls.client = app.test_client()

    def _get(self):
        return self.client.get("/producers/award-intervals")

    def test_returns_200(self):
        self.assertEqual(self._get().status_code, 200)

    def test_response_has_min_and_max_lists(self):
        body = self._get().json
        self.assertIsInstance(body.get("min"), list)
        self.assertIsInstance(body.get("max"), list)

    def test_each_entry_has_required_fields_with_correct_types(self):
        body = self._get().json
        for entry in body["min"] + body["max"]:
            self.assertIsInstance(entry.get("producer"), str)
            self.assertIsInstance(entry.get("interval"), int)
            self.assertIsInstance(entry.get("previousWin"), int)
            self.assertIsInstance(entry.get("followingWin"), int)

    def test_exact_response_matches_proposal_dataset(self):
        body = self._get().json
        self.assertEqual(body["min"], EXPECTED_MIN)
        self.assertEqual(body["max"], EXPECTED_MAX)

    def test_all_min_entries_share_the_same_interval(self):
        body = self._get().json
        self.assertEqual(len({e["interval"] for e in body["min"]}), 1)

    def test_all_max_entries_share_the_same_interval(self):
        body = self._get().json
        self.assertEqual(len({e["interval"] for e in body["max"]}), 1)

    def test_interval_equals_following_minus_previous_win(self):
        body = self._get().json
        for entry in body["min"] + body["max"]:
            self.assertEqual(entry["followingWin"] - entry["previousWin"], entry["interval"])

    def test_csv_loaded_on_startup_produces_non_empty_result(self):
        body = self._get().json
        self.assertGreater(len(body["min"]), 0)
        self.assertGreater(len(body["max"]), 0)
