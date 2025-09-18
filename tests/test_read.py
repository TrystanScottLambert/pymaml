"""
Tests for the read module.
"""

import unittest
import tempfile
import warnings
from pathlib import Path


from pymaml import read_maml


class TestReadMaml(unittest.TestCase):
    """Testing the read MAML function"""

    def setUp(self):
        # Create a temp directory for test files
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_path = Path(self.test_dir.name)

    def tearDown(self):
        # Clean up
        self.test_dir.cleanup()

    def _write_file(self, name: str, content: str) -> str:
        """Helper to write a temporary file with given content."""
        file_path = self.test_path / name
        with open(file_path, "w", encoding="utf8") as f:
            f.write(content)
        return str(file_path)

    def test_valid_maml_file(self):
        """Testing simple case works for simple maml"""
        path = self._write_file("valid.maml", "key: value")
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = read_maml(path)
            self.assertEqual(result, {"key": "value"})
            self.assertEqual(len(w), 0)  # no warnings

    def test_yml_file_warns(self):
        """Testing yaml still read in but warning is given for extension."""
        path = self._write_file("valid.yml", "a: 1")
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = read_maml(path)
            self.assertEqual(result, {"a": 1})
            self.assertTrue(
                any("this is a .yml not a .maml" in str(warn.message) for warn in w)
            )

    def test_invalid_extension_warns(self):
        """Testing that invalid extensions are warned about but still try to be read in."""
        path = self._write_file("data.txt", "c: 3")
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = read_maml(path)
            self.assertEqual(result, {"c": 3})
            self.assertTrue(
                any("extension is not valid" in str(warn.message) for warn in w)
            )

    def test_invalid_yaml_raises_valueerror(self):
        """Testing that non-valid yaml raises an Error"""
        path = self._write_file("broken.maml", "not: [valid_yaml")
        with self.assertRaises(ValueError) as cm:
            read_maml(path)
        self.assertIn("File is not even valid YAML", str(cm.exception))

    def test_empty_file_returns_none(self):
        """Testing empty files"""
        path = self._write_file("empty.maml", "")
        result = read_maml(path)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = read_maml(path)
            self.assertEqual(result, {})
            self.assertTrue(any("FILE IS EMPTY!" in str(warn.message) for warn in w))


if __name__ == "__main__":
    unittest.main()
