import os
import tempfile
import textwrap
from unittest import TestCase

from create_app import create_app
from config import Config


class CsvTestCase(TestCase):
    csv_content: str = ""

    def setUp(self):
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        )
        tmp.write(textwrap.dedent(self.csv_content).strip() + "\n")
        tmp.close()
        self._tmp_path = tmp.name

        class Cfg(Config):
            DATABASE_URL: str = "sqlite:///:memory:"
            CSV_PATH: str = tmp.name
            IN_MEMORY_DB: bool = True

        app = create_app(Cfg())
        app.config["TESTING"] = True
        self.client = app.test_client()

    def tearDown(self):
        os.unlink(self._tmp_path)

    def get_award_intervals(self) -> dict:
        return self.client.get("/producers/award-intervals").json
