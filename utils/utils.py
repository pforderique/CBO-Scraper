import json
import re

import pandas as pd


def parse_json_to_attr(obj, settings_file_path, encoding='utf-8'):
    """loads in settings file and gives the specified object new 
    attributes based on what is included in the file

    Args:
        obj (obejct): object to give new attributes to
        settings_file_path (str): file path of settings file
    """
    with open(settings_file_path, encoding=encoding) as settings_file:
        settings = json.load(settings_file)
        [setattr(obj, attr, val) for (attr, val) in settings.items()]

def clean_string(str: str):
    """Clears 'None' fields and removes html tags from 'str'"""
    if str == 'None': return ''
    return re.sub('</?[a-z]*>', '', str)

def save_to_csv(dicts: list, filename='info'):
    """saves a list of dictionaries with the same keys to a csv with the given
    filename"""
    path = f'./data/{filename}.csv'
    df = pd.DataFrame.from_dict(dicts) 
    df.to_csv (path, index = False, header=True)
