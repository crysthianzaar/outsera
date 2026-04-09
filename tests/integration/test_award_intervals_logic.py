import os
import tempfile

from unittest import TestCase

from create_app import create_app
from config import Config
from tests.integration.csv_test_case import CsvTestCase


class TestMinInterval(CsvTestCase):
    csv_content = """
        year;title;studios;producers;winner
        2000;Film A;S;Producer A;yes
        2001;Film B;S;Producer A;yes
        2000;Film C;S;Producer B;yes
        2010;Film D;S;Producer B;yes
    """

    def test_min_interval_is_1_year(self):
        body = self.get_award_intervals()
        self.assertEqual(body["min"][0]["interval"], 1)
        self.assertEqual(body["min"][0]["producer"], "Producer A")
        self.assertEqual(body["min"][0]["previousWin"], 2000)
        self.assertEqual(body["min"][0]["followingWin"], 2001)


class TestMaxInterval(CsvTestCase):
    csv_content = """
        year;title;studios;producers;winner
        2000;Film A;S;Producer A;yes
        2010;Film B;S;Producer A;yes
        2000;Film C;S;Producer B;yes
        2001;Film D;S;Producer B;yes
    """

    def test_max_interval_is_10_years(self):
        body = self.get_award_intervals()
        self.assertEqual(body["max"][0]["interval"], 10)
        self.assertEqual(body["max"][0]["producer"], "Producer A")
        self.assertEqual(body["max"][0]["previousWin"], 2000)
        self.assertEqual(body["max"][0]["followingWin"], 2010)


class TestTies(CsvTestCase):
    csv_content = """
        year;title;studios;producers;winner
        2000;Film A;S;Producer A;yes
        2001;Film B;S;Producer A;yes
        2010;Film C;S;Producer B;yes
        2011;Film D;S;Producer B;yes
        2000;Film E;S;Producer C;yes
        2010;Film F;S;Producer C;yes
        2005;Film G;S;Producer D;yes
        2015;Film H;S;Producer D;yes
    """

    def test_all_producers_with_min_interval_appear_in_min(self):
        body = self.get_award_intervals()
        self.assertEqual(len(body["min"]), 2)
        self.assertEqual({e["producer"] for e in body["min"]}, {"Producer A", "Producer B"})
        self.assertTrue(all(e["interval"] == 1 for e in body["min"]))

    def test_all_producers_with_max_interval_appear_in_max(self):
        body = self.get_award_intervals()
        self.assertEqual(len(body["max"]), 2)
        self.assertEqual({e["producer"] for e in body["max"]}, {"Producer C", "Producer D"})
        self.assertTrue(all(e["interval"] == 10 for e in body["max"]))


class TestConsecutivePairsOnly(CsvTestCase):
    csv_content = """
        year;title;studios;producers;winner
        2000;Film A;S;Producer A;yes
        2001;Film B;S;Producer A;yes
        2011;Film C;S;Producer A;yes
    """

    def test_3_wins_generates_only_consecutive_pairs_not_total_span(self):
        body = self.get_award_intervals()
        self.assertEqual(body["min"][0]["interval"], 1)
        self.assertEqual(body["min"][0]["previousWin"], 2000)
        self.assertEqual(body["min"][0]["followingWin"], 2001)
        self.assertEqual(body["max"][0]["interval"], 10)
        self.assertEqual(body["max"][0]["previousWin"], 2001)
        self.assertEqual(body["max"][0]["followingWin"], 2011)


class TestSameProducerAppearsMultipleTimesInMin(CsvTestCase):
    csv_content = """
        year;title;studios;producers;winner
        2000;Film A;S;Producer A;yes
        2001;Film B;S;Producer A;yes
        2018;Film C;S;Producer A;yes
        2019;Film D;S;Producer A;yes
    """

    def test_same_producer_appears_twice_when_two_pairs_share_min_interval(self):
        body = self.get_award_intervals()
        self.assertEqual(len(body["min"]), 2)
        self.assertTrue(all(e["interval"] == 1 for e in body["min"]))
        self.assertEqual(
            {(e["previousWin"], e["followingWin"]) for e in body["min"]},
            {(2000, 2001), (2018, 2019)},
        )

    def test_max_is_the_gap_between_the_two_clusters(self):
        body = self.get_award_intervals()
        self.assertEqual(body["max"][0]["interval"], 17)
        self.assertEqual(body["max"][0]["previousWin"], 2001)
        self.assertEqual(body["max"][0]["followingWin"], 2018)


class TestNonWinnersIgnored(CsvTestCase):
    csv_content = """
        year;title;studios;producers;winner
        2000;Film A;S;Producer A;yes
        2001;Film B;S;Producer A;
        2010;Film C;S;Producer A;yes
    """

    def test_nominated_but_not_winner_is_excluded_from_interval_calculation(self):
        body = self.get_award_intervals()
        self.assertEqual(body["min"][0]["interval"], 10)
        self.assertEqual(body["min"][0]["previousWin"], 2000)
        self.assertEqual(body["min"][0]["followingWin"], 2010)


class TestMultipleProducersPerFilm(CsvTestCase):
    csv_content = """
        year;title;studios;producers;winner
        2000;Film A;S;Producer A and Producer B;yes
        2005;Film B;S;Producer A;yes
        2008;Film C;S;Producer B;yes
    """

    def test_each_producer_has_independent_interval_history(self):
        body = self.get_award_intervals()
        self.assertEqual(body["min"][0]["interval"], 5)
        self.assertEqual(body["min"][0]["producer"], "Producer A")
        self.assertEqual(body["max"][0]["interval"], 8)
        self.assertEqual(body["max"][0]["producer"], "Producer B")


class TestAndSeparatorVariants(CsvTestCase):
    csv_content = """
        year;title;studios;producers;winner
        2000;Film A;S;Producer A AND Producer B;yes
        2005;Film B;S;Producer A;yes
        2008;Film C;S;Producer B;yes
    """

    def test_and_separator_is_case_insensitive(self):
        body = self.get_award_intervals()
        self.assertEqual(body["min"][0]["producer"], "Producer A")
        self.assertEqual(body["min"][0]["interval"], 5)
        self.assertEqual(body["max"][0]["producer"], "Producer B")
        self.assertEqual(body["max"][0]["interval"], 8)


class TestOxfordComma(CsvTestCase):
    csv_content = """
        year;title;studios;producers;winner
        2000;Film A;S;Producer A, Producer B, and Producer C;yes
        2005;Film B;S;Producer A;yes
    """

    def test_oxford_comma_before_and_is_handled_correctly(self):
        body = self.get_award_intervals()
        self.assertEqual(body["min"][0]["producer"], "Producer A")
        self.assertEqual(body["min"][0]["interval"], 5)


class TestSingleInterval(CsvTestCase):
    csv_content = """
        year;title;studios;producers;winner
        2000;Film A;S;Producer A;yes
        2007;Film B;S;Producer A;yes
    """

    def test_min_and_max_are_equal_when_only_one_interval_exists(self):
        body = self.get_award_intervals()
        self.assertEqual(body["min"][0]["interval"], 7)
        self.assertEqual(body["max"][0]["interval"], 7)
        self.assertEqual(body["min"], body["max"])


class TestThreeConsecutiveWins(CsvTestCase):
    csv_content = """
        year;title;studios;producers;winner
        2000;Film A;S;Producer A;yes
        2001;Film B;S;Producer A;yes
        2002;Film C;S;Producer A;yes
    """

    def test_three_consecutive_wins_generate_two_pairs_both_in_min_and_max(self):
        body = self.get_award_intervals()
        self.assertEqual(len(body["min"]), 2)
        self.assertEqual(len(body["max"]), 2)
        self.assertTrue(all(e["interval"] == 1 for e in body["min"]))
        self.assertEqual(
            {(e["previousWin"], e["followingWin"]) for e in body["min"]},
            {(2000, 2001), (2001, 2002)},
        )


class TestUtf8Bom(CsvTestCase):
    @classmethod
    def _make_bom_csv(cls) -> str:
        tmp = tempfile.NamedTemporaryFile(mode="wb", suffix=".csv", delete=False)
        content = "year;title;studios;producers;winner\n2000;Film A;S;Producer A;yes\n2005;Film B;S;Producer A;yes\n"
        tmp.write(b"\xef\xbb\xbf")
        tmp.write(content.encode("utf-8"))
        tmp.close()
        return tmp.name

    def setUp(self):
        self._bom_path = self._make_bom_csv()

        class Cfg(Config):
            DATABASE_URL: str = "sqlite:///:memory:"
            CSV_PATH: str = self._bom_path
            IN_MEMORY_DB: bool = True

        app = create_app(Cfg())
        app.config["TESTING"] = True
        self.client = app.test_client()

    def tearDown(self):
        os.unlink(self._bom_path)

    def test_csv_with_utf8_bom_is_read_without_error(self):
        response = self.client.get("/producers/award-intervals")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["min"][0]["interval"], 5)


class TestIntervalInvariants(CsvTestCase):
    csv_content = """
        year;title;studios;producers;winner
        1980;Film A;S;Producer A;yes
        1999;Film B;S;Producer A;yes
        2000;Film C;S;Producer B;yes
        2001;Film D;S;Producer B;yes
        2010;Film E;S;Producer C;yes
        2011;Film F;S;Producer C;yes
        2020;Film G;S;Producer D;yes
        2025;Film H;S;Producer D;yes
    """

    def test_following_win_minus_previous_win_always_equals_interval(self):
        body = self.get_award_intervals()
        for entry in body["min"] + body["max"]:
            self.assertEqual(entry["followingWin"] - entry["previousWin"], entry["interval"])

    def test_all_min_entries_share_the_same_interval_value(self):
        body = self.get_award_intervals()
        self.assertEqual(len({e["interval"] for e in body["min"]}), 1)

    def test_all_max_entries_share_the_same_interval_value(self):
        body = self.get_award_intervals()
        self.assertEqual(len({e["interval"] for e in body["max"]}), 1)
