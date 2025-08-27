"""
Tests for the read module.
"""

import os
import tempfile
import unittest
import warnings
from unittest.mock import patch

import yaml

from pymaml import read


class TestReadMaml(unittest.TestCase):
    """
    Unit tests for read_maml.read_maml
    """

    def setUp(self):
        warnings.simplefilter("always")

    def make_temp_file(self, suffix=".maml", content=None):
        """Helper to create a temporary file with given suffix and YAML content"""
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix, mode="w", encoding="utf8")
        if content is not None:
            yaml.dump(content, tmp)
        tmp.close()
        return tmp.name

    def test_simple_valid_maml(self):
        """Simple case: correct .maml file and valid content"""
        data = {"key": "value"}
        path = self.make_temp_file(".maml", data)

        with patch("read.is_valid", return_value=True):
            with warnings.catch_warnings(record=True) as w:
                result = read.read_maml(path)

        self.assertEqual(result, data)
        self.assertEqual(len(w), 0)  # no warnings

        os.remove(path)

    def test_yaml_extension_warns(self):
        """File with .yml extension should still load but give warning"""
        data = {"foo": "bar"}
        path = self.make_temp_file(".yml", data)

        with patch("read.is_valid", return_value=True):
            with warnings.catch_warnings(record=True) as w:
                result = read.read_maml(path)

        self.assertEqual(result, data)
        self.assertTrue(any("this is a .yml not a .maml" in str(warn.message) for warn in w))

        os.remove(path)

    def test_incorrect_extension_warns(self):
        """File with wrong extension but valid MAML should warn"""
        data = {"baz": 123}
        path = self.make_temp_file(".txt", data)

        with patch("read.is_valid", return_value=True):
            with warnings.catch_warnings(record=True) as w:
                result = read.read_maml(path)

        self.assertEqual(result, data)
        self.assertTrue(any("missing correct extension" in str(warn.message) for warn in w))

        os.remove(path)

    def test_invalid_content_warns(self):
        """Invalid content should produce validation warning"""
        data = {"invalid": "data"}
        path = self.make_temp_file(".maml", data)

        with patch("read.is_valid", return_value=False):
            with warnings.catch_warnings(record=True) as w:
                result = read.read_maml(path)

        self.assertEqual(result, data)
        self.assertTrue(any("IS NOT VALID MAML" in str(warn.message) for warn in w))

        os.remove(path)

    def test_file_not_found_raises(self):
        """Non-existent file should raise FileNotFoundError"""
        with self.assertRaises(FileNotFoundError):
            read.read_maml("does_not_exist.maml")

    def test_invalid_yaml_raises(self):
        """File with bad YAML content should raise yaml.YAMLError"""
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".maml", mode="w", encoding="utf8")
        tmp.write("this: is: not: valid: yaml: [")  # deliberately broken YAML
        tmp.close()

        with self.assertRaises(yaml.YAMLError):
            read.read_maml(tmp.name)

        os.remove(tmp.name)


if __name__ == "__main__":
    unittest.main()
