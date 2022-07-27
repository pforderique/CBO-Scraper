import json

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