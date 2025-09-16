"""
Unit tests for the v1p0 class
"""

import unittest
import yaml

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


if __name__ == "__main__":
    unittest.main()
