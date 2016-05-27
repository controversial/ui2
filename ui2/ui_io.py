""" Utilities for writing and reading .pyui2 files """


import json


def _json_get(inp):
    """ Get a Python object (list or dict) regardless of whether data is passed
    as a JSON string, a file path, or is already a python object.
    
    Returns the parsed data, as well as "native" if the data was already a
    Python object, "str" if the data was passed as a JSON string, or the path
    if the data passed was a file path """
    
    if not (isinstance(inp, dict) or isinstance(inp, list)):  # Python object
        try:                                                    # JSON string
            data = json.loads(inp)
            dataformat = "str"
        except json.JSONDecodeError:                            # JSON filepath
            # Store the filename in the dataformat variable if dataformat is a
            # file,  because it's just one fewer variable to keep track of
            dataformat = inp
            with open(inp, encoding="utf-8") as f:
                data = json.load(f)
    else:
        dataformat = "native"
    
    return data, dataformat


def embed_custom_attributes(inp, data):
    """ ui2 stores metadata by embedding a `ui2` key in the `attributes` dict
    of the base view. This function automates the storing of said "custom
    attributes." Pass a JSON string, a dict, or the path to a pyui file """

    # Load dict, storing the format of `.pyui` used (JSON filename,
    # JSON string, or Python object)
    pyui, dataformat = _json_get(inp)

    pyui[0]["attributes"]["ui2"] = data

    if dataformat == "native":
        return pyui
    elif dataformat == "str":
        return json.dumps(pyui, indent=2)
    else:
        with open(dataformat, "w", encoding="utf-8") as f:
            json.dump(pyui, f, indent=2)


def get_custom_attributes(pyui):
    pyui, dataformat = _json_get(pyui)
    return pyui[0]["attributes"]["ui2"]
