"""
Testing the main MAML class
"""

import unittest
import tempfile
import os
import warnings
from unittest.mock import patch

import yaml

from maml import Field, MAML, FIELD_KEY_ORDER, MAML_KEY_ORDER


class TestField(unittest.TestCase):
    """Testing that the field class works."""
    def test_from_dict_all_keys(self):
        """Testing that assinging keys from dict works"""
        data = {"name": "flux", "data_type": "float", "unit": "Jy", "description": "flux density", "ucd": None}
        field = Field.from_dict(data)
        self.assertEqual(field.name, "flux")
        self.assertEqual(field.data_type, "float")
        self.assertEqual(field.unit, "Jy")
        self.assertEqual(field.description, "flux density")
        self.assertIsNone(field.ucd)

    def test_from_dict_missing_recommended_warns(self):
        """Checking the warnings"""
        data = {"name": "flux", "data_type": "float"}
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            _ = Field.from_dict(data)
        self.assertTrue(any("Recomended property" in str(warn.message) for warn in w))

    def test_from_dict_invalid_ucd_raises(self):
        """Checking invalid ucd"""
        data = {"name": "flux", "data_type": "float", "ucd": "invalid_ucd"}
        with self.assertRaises(AttributeError):
            Field.from_dict(data)

    def test_from_dict_missing_required_keys_raises(self):
        """Check that missing the wrong keys crash"""
        data = {"name": "flux"}  # missing data_type
        with self.assertRaises(AttributeError):
            Field.from_dict(data)


class TestMAML(unittest.TestCase):
    def setUp(self):
        # minimal maml dict
        self.valid_dict = {
            "table": "my_table",
            "author": "Dr. Example",
            "fields": [{"name": "flux", "data_type": "float"}]
        }

    @patch("maml.read_maml")
    @patch("maml.is_valid", return_value=True)
    def test_from_file_valid(self, mock_valid, mock_read):
        mock_read.return_value = self.valid_dict
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            maml_obj = MAML.from_file("dummy.maml")
        self.assertEqual(maml_obj.table, "my_table")
        self.assertEqual(maml_obj.author, "Dr. Example")
        self.assertEqual(len(maml_obj.fields), 1)
        self.assertIsInstance(maml_obj.fields[0], Field)

    @patch("maml.read_maml")
    @patch("maml.is_valid", return_value=False)
    def test_from_file_invalid_raises(self, mock_valid, mock_read):
        mock_read.return_value = self.valid_dict
        with self.assertRaises(AttributeError):
            MAML.from_file("dummy.maml")

    def test_to_dict_key_order(self):
        field = Field(name="flux", data_type="float")
        maml_obj = MAML(table="tab", author="auth", fields=[field])
        d = maml_obj.to_dict()
        self.assertEqual(list(d.keys()), MAML_KEY_ORDER)
        self.assertEqual(list(d["fields"][0].keys()), FIELD_KEY_ORDER)

    def test_to_file_writes_yaml(self):
        field = Field(name="flux", data_type="float")
        maml_obj = MAML(table="tab", author="auth", fields=[field])
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".maml")
        tmp_file.close()
        try:
            maml_obj.to_file(tmp_file.name)
            # check that file exists and is valid YAML
            with open(tmp_file.name, "r", encoding="utf8") as f:
                data = yaml.safe_load(f)
            self.assertIn("table", data)
            self.assertIn("fields", data)
        finally:
            os.remove(tmp_file.name)

    def test_to_file_invalid_extension_raises(self):
        field = Field(name="flux", data_type="float")
        maml_obj = MAML(table="tab", author="auth", fields=[field])
        with self.assertRaises(ValueError):
            maml_obj.to_file("file.txt")


if __name__ == "__main__":
    unittest.main()
