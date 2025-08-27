"""
Helper module to parse and check valid maml data structures.
"""

import datetime

REQUIRED_META_DATA = ["table", "version", "date", "author", "fields"]
RECOMENDED_META_DATA = ["survey", "dataset"]

REQURED_FIELD_META_DATA = ["name", "datatype"]
RECOMENDED_FIELD_META_DATA = ["unit", "description", "ucd"]


def is_iso8601(date: str) -> bool:
    """
    Validates that the given date is in the ISO 8601 format (https://en.wikipedia.org/wiki/ISO_8601)
    """
    try:
        datetime.datetime.fromisoformat(date)
        return True
    except ValueError:
        return False


def is_valid(maml_data: dict) -> bool:
    """
    Checks if the dict is a valid representation of maml data
    """
    if not isinstance(maml_data, dict):
        return False
    try:
        for required in REQUIRED_META_DATA:
            _ = maml_data[required]

        fields = maml_data["fields"]
        for required in RECOMENDED_FIELD_META_DATA:
            _ = fields[required]
    except KeyError:
        return False

    return is_iso8601(maml_data["date"])
