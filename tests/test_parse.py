"""
Tests for the parse module
"""

import unittest
import datetime

from pymaml import is_iso8601

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


if __name__ == "__main__":
    unittest.main()
