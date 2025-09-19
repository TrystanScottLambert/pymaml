"""
Tests for the parse module
"""

import unittest
import datetime

from pymaml import is_iso8601, valid_for
from pymaml.parse import check_order


class TestIsISO8601(unittest.TestCase):
    """Testing correct iso dates are validated correctly"""

    def test_valid_dates(self):
        """Valid ISO8601 dates should return True"""
        valid_dates = ["2025-01-01", "1999-12-31", datetime.date.today().isoformat()]
        for d in valid_dates:
            with self.subTest(date=d):
                self.assertTrue(is_iso8601(d))

    def test_invalid_dates(self):
        """Invalid ISO8601 dates should return False"""
        invalid_dates = [
            "2025/01/01",  # wrong separator
            "01-01-2025",  # wrong order
            "2025-13-01",  # invalid month
            "2025-00-10",  # invalid month
            "2025-01-32",  # invalid day
            "not-a-date",  # junk string
            "",  # empty string
        ]
        for d in invalid_dates:
            with self.subTest(date=d):
                self.assertFalse(is_iso8601(d))


class TestValidFor(unittest.TestCase):
    """Testing the valid for function"""

    def test_valid_v10(self):
        """Testing that earlier versions are still validated by later versions"""
        valids = valid_for("tests/example_v1p0.maml")
        self.assertEqual(len(valids), 2)
        self.assertEqual(valids[0], "v1.0")
        self.assertEqual(valids[1], "v1.1")

    def test_valid_v11(self):
        """Testing that for later versions only later versions pass."""
        valids = valid_for("tests/example_v1p1.maml")
        self.assertEqual(len(valids), 1)
        self.assertEqual(valids[0], "v1.1")

    def test_not_valid(self):
        """Testing that when we pass non valid stuff that a non valid arises."""
        valids = valid_for("tests/invalid.maml")
        self.assertEqual(len(valids), 1)
        self.assertEqual("Not valid for any version of MAML", valids[0])


class TestOrder(unittest.TestCase):
    """
    Testing the check_order function.
    """

    def test_10_correct(self):
        """Testing that v1.0 returns true for the correct orders."""
        correct = {
            "survey": 1,
            "author": 2,
            "DOIs": [{"DOI": 1, "type": 1}],
            "fields": [{"name": 1, "unit": 1, "data_type": 1}],
        }
        res = check_order(correct, "v1.0")
        self.assertTrue(res)

    def test_11_correct(self):
        """Testing that v1.1 returns true for the correct orders."""
        correct = {
            "survey": 1,
            "author": 2,
            "DOIs": [{"DOI": 1, "type": 1}],
            "extra": 1,
            "fields": [{"name": 1, "unit": 1, "data_type": 1}],
        }
        res = check_order(correct, "v1.1")
        self.assertTrue(res)

    def test_10_incorrect(self):
        """Testing that v1.0 returns false for incorrect orders."""
        correct = {
            "survey": 1,
            "author": 2,
            "DOIs": [{"DOI": 1, "type": 1}],
            "fields": [{"name": 1, "data_type": 1, "unit": 1}],  # unit in wrong place.
        }
        res = check_order(correct, "v1.0")
        self.assertFalse(res)

    def test_11_incorrect(self):
        """Testing that v1.1 returns false for incorrect orders."""
        correct = {
            "survey": 1,
            "author": 2,
            "DOIs": [{"DOI": 1, "type": 1}],
            "fields": [{"name": 1, "data_type": 1, "unit": 1}],
            "extra": 1,
        }
        res = check_order(correct, "v1.1")
        self.assertFalse(res)


if __name__ == "__main__":
    unittest.main()
