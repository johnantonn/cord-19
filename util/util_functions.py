""" This module contains auxiliary python files and classes """

import json
import os
from pathlib import Path


def read_json_file(filepath):
    """ Function that reads a json file and returns a dictionary.

    Args:
        filepath (str): The path of the json file

    Returns:
        (dict): The dictionary with the contents of the json file
    """

    try:
        if not os.path.exists(filepath):
            raise FileNotFoundError("filepath %s does not exist" % filepath)

        with open(filepath) as f:
            file_content = json.load(f)
    except json.JSONDecodeError:
        return None

    return file_content


def write_json_to_file(json_data, filepath):
    """ Function that writes json content to a file.

    Args:
        json_data (dict): The input dictionary
        filepath (str): The filepath of the new file
    """
    try:
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
        with open(filepath, 'w') as json_file:
            json.dump(json_data, json_file)
    except TypeError:
        return None


def get_subfolders_and_files(input_folder, file_type):
    """ Function that returns the subdirectories of a given folder
    and the files of the given type.

    Args:
        input_folder (str): The path of the given folder
        file_type (str): The required type of the files

    Returns:
        (list): A list of the files of the given type along with their parent folders
    """

    json_files = list()
    for path in Path(input_folder).rglob('*.' + file_type):
        json_files.append(path.absolute())

    return json_files
