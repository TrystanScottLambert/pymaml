"""
Test maml
"""

import unittest
from pymaml import MAML
from pymaml.maml import Field


class TestMAML(unittest.TestCase):
    """
    Main testing class
    """

    def test_default(self):
        """
        Testing that the default generation is sufficient.
        """
        result = MAML.default()
        result = result.__dict__
        answer = {
            "table": "Table Name",
            "author": "Lead Author <email>",
            "fields": [
                Field(
                    name="RA",
                    data_type="float",
                    unit="deg",
                    description="Right Ascension",
                    ucd="pos.eq.ra",
                ),
                Field(
                    name="Dec",
                    data_type="float",
                    unit="deg",
                    description="Declination",
                    ucd="pos.eq.dec",
                ),
            ],
            "survey": "Survey Name",
            "dataset": "Dataset Name",
            "version": "0.0.1",
            "date": "1995-12-09",
            "coauthors": ["Co-Author 1 <email1>", "Co-Author 2 <email2>"],
            "depend": [
                "Dataset 1 depends on [optional]",
                "Dataset 2 depends on [optional]",
            ],
            "comment": ["Something 1", "Something 2"],
        }
        for res, ans in zip(result, answer):
            self.assertEqual(res, ans)

    def test_set_date(self):
        """
        Testing that the set date will only accept correct formats.
        """
        maml = MAML.default()

        # Check for correct date format
        maml.set_date("2025-01-01")
        self.assertEqual(maml.date, "2025-01-01")

        # Check that error is raised for incorrect format.
        with self.assertRaises(ValueError):
            maml.set_date("2025-13-01")

    def test_set_field(self):
        """
        Checking that we can append a field and all errors occur when we need them to.
        """
        maml = MAML.default()
        fields = maml.fields

        # Simple add
        maml.add_field(name="redshift", data_type="float")
        fields.append(Field(name="redshift", data_type="float"))
        self.assertEqual(fields, maml.fields)

        # Check that invalid ucd isn't accepted
        with self.assertRaises(AttributeError):
            maml.add_field(name='test', data_type='test', ucd = 'not.valid.hello')

    def test_add_comment(self):
        """
        Testing that the add comment will parse the string.
        """
        maml = MAML.default()
        maml.add_comment(5)
        self.assertEqual(maml.comment[-1], "5")
