"""
Module to test the reading module.
"""

import unittest


class TestReadFunction:
    """
    Testing the read maml file.
    """

    def test_simple(self):
        """
        simple reading a correct maml file
        """

    def test_yaml(self):
        """
        Simple read a maml file with the incorrect yaml extension and gives a warning
        """

    def test_incorrect_extension(self):
        """
        Test warning for when the extension is incorrect but the file is still valid maml
        """

    def test_wrong_file(self):
        """
        Testing that the wrong file format with the wrong extension causes an error
        """


if __name__ == "__main__":
    unittest.main()
