"""
Test maml
"""

import os
import unittest
import yaml

import pandas as pd

from pymaml.maml import MAML, MAMLBuilder, _assert_version
from pymaml import V1P1, today


class TestMAML(unittest.TestCase):
    """
    Main testing class
    """

    def test_read_from_file(self):
        """
        Testing that the class can be constructed from a valid maml file.
        """
        test_maml_10 = MAML.from_file("tests/example_v1p0.maml", "v1.0")
        test_maml_11 = MAML.from_file("tests/example_v1p1.maml", "v1.1")

        self.assertEqual(test_maml_10.version, "v1.0")
        self.assertEqual(
            test_maml_10.meta.version, "Required version (string, integer, or float)"
        )

        self.assertEqual(test_maml_11.meta.keywords, ["Optional keyword tag", "..."])
        self.assertEqual(len(test_maml_11.meta.keyarray), 3)

    def test_created_from_dict(self):
        """
        Testing that object can be created from a dictionary
        """
        with open("tests/example_v1p1.maml", encoding="utf8") as file:
            example_dict = yaml.safe_load(file)

        test_maml = MAML(example_dict, "v1.1")
        from_file_maml = MAML.from_file("tests/example_v1p1.maml", "v1.1")
        ans_dict = from_file_maml.__dict__
        res_dict = test_maml.__dict__
        self.assertDictEqual(ans_dict, res_dict)

    def test_to_file(self):
        """
        Testing that the to_file creates valid maml.
        """
        test_maml = MAML.from_file("tests/example_v1p0.maml", "v1.0")
        test_maml.to_file("test.maml")
        with self.assertRaises(ValueError):
            test_maml.to_file("test.notgoingtowork")
        read_back_in = MAML.from_file("test.maml", "v1.0")
        self.assertDictEqual(test_maml.__dict__, read_back_in.__dict__)
        os.remove("test.maml")

    def test_to_markdown(self):
        """
        Testing that the to_markdown method creates a valid markdown file.
        """
        test_maml = MAML.from_file("tests/example_v1p0.maml", "v1.0")
        test_maml_v1p1 = MAML.from_file("tests/example_v1p1.maml", "v1.1")
        test_maml.to_markdown("test_markdown_v1p0.md")
        test_maml_v1p1.to_markdown("test_markdown_v1p1.md")

        with open("tests/example_markdown_v1p1.md", encoding="utf8") as file:
            answer_v1p1 = file.read()

        with open("tests/example_markdown_v1p0.md", encoding="utf8") as file:
            answer_v1p0 = file.read()

        with open("test_markdown_v1p0.md", encoding="utf8") as file:
            result_v1p0 = file.read()
        with open("test_markdown_v1p1.md", encoding="utf8") as file:
            result_v1p1 = file.read()

        self.assertEqual(answer_v1p1.strip(), result_v1p1.strip())
        self.assertEqual(answer_v1p0.strip(), result_v1p0.strip())
        os.remove("test_markdown_v1p0.md")
        os.remove("test_markdown_v1p1.md")

    def test_to_dict(self):
        """
        Testing that the object can be represented as a dictionary
        """
        example_file = "tests/example_v1p1.maml"
        test_maml = MAML.from_file(example_file, "v1.1")
        res_dict = test_maml.to_dict()

        with open(example_file, encoding="utf8") as file:
            ans_dict = yaml.safe_load(file)
        self.assertDictEqual(ans_dict, res_dict)


class TestBuilder(unittest.TestCase):
    """
    Main class testing the Builder pattern is working correctly.
    """

    def test_simple_building(self):
        """
        Testing that initilization, setting, and adding is working correctly.
        """
        # Init
        builder = MAMLBuilder("v1.1")
        self.assertEqual(builder.version, "v1.1")
        self.assertTrue(isinstance(builder._model_cls, type(V1P1)))
        self.assertDictEqual(builder._data, {})

        # Setting
        builder.set("Test", "Something")
        builder.set("Should", "Work")
        self.assertDictEqual(builder._data, {"Test": "Something", "Should": "Work"})

        builder.set("Test", "Something Else")
        self.assertDictEqual(
            builder._data, {"Test": "Something Else", "Should": "Work"}
        )

        # Adding
        builder.add("List", "This should be in a list")
        builder.add("List", "So should this")
        builder.add("another_list", "only this one in the list")
        ans_dict = {
            "Test": "Something Else",
            "Should": "Work",
            "List": ["This should be in a list", "So should this"],
            "another_list": ["only this one in the list"],
        }
        self.assertDictEqual(builder._data, ans_dict)

    def test_build(self):
        """
        Test building a valid maml.
        """
        builder = MAMLBuilder("v1.0")
        builder.set("version", "beta")
        builder.set("table", "Name of Table")
        builder.set("date", "2025-09-11")
        builder.add("fields", {"name": "test", "data_type": "random"})
        builder.set("author", "ME")
        builder.add(
            "fields", {"name": "another test", "unit": "km/s", "data_type": "random"}
        )
        maml = builder.build()

        ans_dict = {
            "table": "Name of Table",
            "version": "beta",
            "date": "2025-09-11",
            "author": "ME",
            "MAML_version": 1.0,
            "fields": [
                {"name": "test", "data_type": "random"},
                {"name": "another test", "unit": "km/s", "data_type": "random"},
            ],
        }
        self.assertDictEqual(maml.to_dict(include_none=False), ans_dict)


class TestAssertVersion(unittest.TestCase):
    """
    Testing that the _assert_version will crash correctly for wrong versions
    """

    def test_valid(self):
        """When the value is correct"""
        _assert_version("v1.0")
        _assert_version("v1.1")
        self.assertEqual(1, 1)

    def test_not_valid(self):
        """When the value is not correct"""
        self.assertRaises(ValueError, _assert_version, "v1p1")


class TestBuilderDefaults(unittest.TestCase):
    """
    Testing that the buiders work with defaults.
    """

    def test_v10(self):
        """Testing that version 1.0 generates defaults with the builder."""
        builder = MAMLBuilder("v1.0", defaults=True)
        res = builder._data
        self.assertEqual(res["table"], "__REQUIRED__: Table Name")
        self.assertEqual(res["version"], "__REQUIRED__: 0.1.0")
        self.assertEqual(res["date"], today())
        self.assertEqual(res["author"], "__REQUIRED__: Main Author")
        self.assertEqual(len(res["fields"]), 1)
        self.assertEqual(res["fields"][0]["name"], "__REQUIRED__: field name")
        self.assertEqual(res["fields"][0]["data_type"], "__REQUIRED__: data_type")
        with self.assertRaises(KeyError):
            _ = res["keyarray"]

    def test_v11(self):
        """Testing that version 1.1 generates defaults with the builder."""
        builder = MAMLBuilder("v1.1", defaults=True)
        res = builder._data
        self.assertEqual(res["table"], "__REQUIRED__: Table Name")
        self.assertEqual(res["version"], "__REQUIRED__: 0.1.0")
        self.assertEqual(res["date"], today())
        self.assertEqual(res["author"], "__REQUIRED__: Main Author")
        self.assertEqual(len(res["fields"]), 1)
        self.assertEqual(res["fields"][0]["name"], "__REQUIRED__: field name")
        self.assertEqual(res["fields"][0]["data_type"], "__REQUIRED__: data_type")
        self.assertIsNone(res["keyarray"])


class TestMAMLBuilderHelpers(unittest.TestCase):
    """
    Testing all the MAML builder helper functions
    """

    def test_listing_meta_data(self):
        """
        Testing that all the possible fields are listed out for the user.
        """
        builder = MAMLBuilder("v1.1")
        res = builder.possible_metadata()
        ans = [
            "survey",
            "dataset",
            "table",
            "version",
            "date",
            "author",
            "coauthors",
            "DOIs",
            "depends",
            "description",
            "comments",
            "license",
            "keywords",
            "keyarray",
            "extra",
            "MAML_version",
            "fields",
        ]
        for r, a in zip(res, ans):
            self.assertEqual(r, a)

    def test_adding(self):
        """Testing that we can edit list entries using the edit method."""
        builder = MAMLBuilder("v1.1", defaults=True)
        builder.add("DOIs", "testtest")
        builder.add("DOIs", "more_tests")
        self.assertEqual(builder._data["DOIs"][0], "testtest")
        self.assertEqual(builder._data["DOIs"][1], "more_tests")


class TestBuilderFieldsFromPandas(unittest.TestCase):
    """Testing that we can build the fields from pandas dataframes"""

    def setUp(self):
        self.builder = MAMLBuilder("v1.1")

    def test_basic_dataframe(self):
        """Simple case"""
        df = pd.DataFrame(
            {"id": [1, 2, 3], "value": [0.1, 0.2, 0.3], "name": ["a", "b", "c"]}
        )

        self.builder.fields_from_pandas(df)

        expected_fields = [
            {"name": "id", "data_type": "int64"},
            {"name": "value", "data_type": "float64"},
            {"name": "name", "data_type": "object"},
        ]

        self.assertEqual(self.builder._data["fields"], expected_fields)

    def test_empty_dataframe(self):
        df = pd.DataFrame()

        self.builder.fields_from_pandas(df)

        # Should stay empty
        self.assertEqual(self.builder._data.get("fields", []), [])

    def test_weird_column_names(self):
        df = pd.DataFrame({"Column With Space": [1, 2], "special!char$": ["x", "y"]})

        self.builder.fields_from_pandas(df)

        expected_fields = [
            {"name": "Column With Space", "data_type": "int64"},
            {"name": "special!char$", "data_type": "object"},
        ]

        self.assertEqual(self.builder._data["fields"], expected_fields)


if __name__ == "__main__":
    unittest.main()
