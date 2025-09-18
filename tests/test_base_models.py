"""
Unit tests for the v1p0 class
"""

import unittest
import yaml
from pydantic import ValidationError

from pymaml import V1P0, V1P1


class Read(unittest.TestCase):
    """
    Class to read the official examples and confirm that they being validated correctly.
    """

    def test_read_in_v1p0(self):
        """
        Reading in the example file for v1.0. Not expecting any errors.
        """
        with open("tests/example_v1p0.maml", encoding="utf8") as file:
            data = yaml.safe_load(file)

        metadata = V1P0(**data)
        self.assertEqual(
            metadata.license, "Recommended license for the dataset / table"
        )
        self.assertEqual(metadata.survey, "Optional survey name")
        self.assertEqual(
            metadata.version, "Required version (string, integer, or float)"
        )

    def test_read_in_v1p1(self):
        """
        Reading in the example file for v1.1. Not expecting any errors.
        """
        with open("tests/example_v1p0.maml", encoding="utf8") as file:
            data = yaml.safe_load(file)

        metadata = V1P1(**data)
        self.assertEqual(
            metadata.license, "Recommended license for the dataset / table"
        )
        self.assertEqual(metadata.survey, "Optional survey name")
        self.assertEqual(
            metadata.version, "Required version (string, integer, or float)"
        )


class TestFieldEntryUCD(unittest.TestCase):
    """Testing that only valid ucd is accepted."""

    def test_valid_ucd(self):
        """A valid UCD should pass validation"""
        data = {
            "table": "table",
            "version": 0,
            "date": "1995-09-12",
            "author": "me",
            "fields": [{"name": "test", "data_type": "float", "ucd": "pos.eq.ra"}],
        }
        v1p0_test = V1P0(**data)
        v1p1_test = V1P1(**data)
        self.assertEqual(v1p0_test.fields[0].ucd, "pos.eq.ra")
        self.assertEqual(v1p1_test.fields[0].ucd, "pos.eq.ra")

    def test_invalid_ucd(self):
        """An invalid UCD should raise a validation error"""
        data = {
            "table": "table",
            "version": 0,
            "date": "1995-09-12",
            "author": "me",
            "fields": [{"name": "test", "data_type": "float", "ucd": "not.valid"}],
        }

        with self.assertRaises(ValidationError):
            V1P0(**data)

        with self.assertRaises(ValidationError):
            V1P1(**data)


if __name__ == "__main__":
    unittest.main()
