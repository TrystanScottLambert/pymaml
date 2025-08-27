"""
Tests for the parse module
"""

import unittest
import datetime
from parse import is_iso8601, is_valid


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
            "2025/01/01",    # wrong separator
            "01-01-2025",    # wrong order
            "2025-13-01",    # invalid month
            "2025-00-10",    # invalid month
            "2025-01-32",    # invalid day
            "not-a-date",    # junk string
            "",              # empty string
        ]
        for d in invalid_dates:
            with self.subTest(date=d):
                self.assertFalse(is_iso8601(d))


class TestIsValid(unittest.TestCase):
    """Testing that the valid maml function works correcly"""
    def make_valid_maml(self, date=None):
        """Helper to create a minimal valid maml dict"""
        if date is None:
            date = datetime.date.today().isoformat()
        return {
            "table": "my_table",
            "version": "1.0",
            "date": date,
            "author": "Dr. Example",
            "fields": [
                {"name": "flux", "data_type": "float"}
            ],
        }

    def test_valid_dict(self):
        """Valid maml dict should return True"""
        data = self.make_valid_maml()
        self.assertTrue(is_valid(data))

    def test_not_a_dict(self):
        """Non-dict input should return False"""
        for bad in [None, [], "string", 42]:
            with self.subTest(value=bad):
                self.assertFalse(is_valid(bad))

    def test_missing_required_top_level_keys(self):
        """Missing required metadata keys should return False"""
        for missing in ["table", "version", "date", "author", "fields"]:
            data = self.make_valid_maml()
            data.pop(missing)
            with self.subTest(missing=missing):
                self.assertFalse(is_valid(data))

    def test_missing_required_field_keys(self):
        """Missing required keys inside fields should return False"""
        for missing in ["name", "data_type"]:
            data = self.make_valid_maml()
            data["fields"][0].pop(missing)
            with self.subTest(missing=missing):
                self.assertFalse(is_valid(data))

    def test_invalid_date(self):
        """Invalid date should return False"""
        data = self.make_valid_maml(date="not-a-date")
        self.assertFalse(is_valid(data))


if __name__ == "__main__":
    unittest.main()
