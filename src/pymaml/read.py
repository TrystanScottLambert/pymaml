"""
Main module for reading maml files.
"""
import warnings
import os

import yaml


warnings.formatwarning = lambda msg, *args, **kwargs: f"{msg}\n"

def read_maml(file_name: str) -> dict:
    """
    Reads in a maml file and warns for strange extensions.
    """
    _, extension = os.path.splitext(file_name)
    match extension:
        case '.yml' | '.yaml':
            warnings.warn("WARNING: File was read in but this is a .yml not a .maml\n")
        case '.maml':
            pass
        case _:
            warnings.warn("WARNING: Attempting to read in file but extension is not valid.")
    with open(file_name, encoding='utf8') as file:
        maml_dict = yaml.safe_load(file)
    return maml_dict
