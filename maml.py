"""
Main maml object.
"""

import warnings
from dataclasses import dataclass

from astropy.io.votable.ucd import check_ucd

from parse import today, is_valid, RECOMENDED_META_DATA, OPTIONAL_META_DATA
from read import read_maml


@dataclass
class Field:
    """
    Class storing the field data
    """

    name: str
    data_type: str
    description: str = None
    ucd: str = None

    def __post_init__(self):
        if self.ucd is not None:
            if not check_ucd(self.ucd, check_controlled_vocabulary=True):
                raise AttributeError(f"{self.ucd} is not valid ucd.")

    @classmethod
    def from_dict(cls, dictionary: dict[str, str]):
        """
        Constructs a field object from a dictionary.
        """
        try:
            name = dictionary["name"]
            datatype = dictionary["data_type"]
        except KeyError as exc:
            raise AttributeError(
                "Dictionary object does not have the correct values to be read in as a field."
            ) from exc
        value = cls(name=name, data_type=datatype)
        try:
            value.description = dictionary["description"]
        except KeyError:
            warnings.warn(f"No description found in dictionary for {name} field")

        try:
            ucd = dictionary["ucd"]
            if not check_ucd(ucd, check_controlled_vocabulary=True):
                raise AttributeError(f"{ucd} is not valid ucd")
            value.ucd = ucd
        except KeyError:
            warnings.warn(f"No ucd found in dictionary for {name} field")

        return value


@dataclass
class MAML:
    """
    Class for storing maml data.
    """

    table: str
    author: str
    fields: list[Field]
    survey: str = None
    dataset: str = None
    version: str = "0.1.0"
    date: str = today()
    coauthors: list[str] = None
    depend: list[str] = None
    comment: list[str] = None

    @classmethod
    def from_file(cls, file_name: str) -> None:
        """
        Creates a MAML object from file.
        """
        dictionary = read_maml(file_name)
        if not is_valid(dictionary):
            raise AttributeError(f"{file_name} is not a valid maml file.")

        fields = [Field.from_dict(field) for field in dictionary["fields"]]
        value = cls(
            table=dictionary["table"], author=dictionary["author"], fields=fields
        )
        for recommended in RECOMENDED_META_DATA:
            if recommended in dictionary:
                setattr(value, recommended, dictionary[recommended])
            else:
                warnings.warn(f"Recommended value {recommended} not found in file.")

        for optional in OPTIONAL_META_DATA:
            if optional in dictionary:
                setattr(value, optional, dictionary[optional])

        return value
