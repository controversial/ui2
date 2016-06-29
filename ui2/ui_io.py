""" Utilities for writing and reading custom info from .pyui files """


import json
import uuid


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


def view_to_dict(view):
    """ The magical solution to store ui.View instances as pyui files """
    # The base attributes shared across all views
    out = {
        "selected": False,
        # This is a scary amount of curly braces, but Python format syntax
        # requires double curly braces for one to appear in the result.
        "frame": "{{{{{}, {}}}, {{{}, {}}}}}".format(int(view.frame.min_x),
                                                     int(view.frame.min_y),
                                                     int(view.frame.width),
                                                     int(view.frame.height)),
        "class": view.__class__.__name__,
        "nodes": [view_to_dict(sv) for sv in view.subviews],
        "attributes": {}
    }

    # Add the strange attributes. Some of these are duplicate properties, and
    # some are never used at all as far as I can tell (like 'uuid') I'm
    # including them to be safe, though.
    out["attributes"]["uuid"] = uuid.uuid4()
    out["attributes"]["class"] = view.__class__.__name__
    out["attributes"]["frame"] = out["frame"]

    # Add the easy attributes
    attrs = ["custom_class", "root_view_name", "background_color",
             "title_color", "title_bar_color", "flex", "alpha", "name",
             "tint_color", "border_width", "border_color", "corner_radius",
             "font_name", "font_size", "alignment", "number_of_lines",
             "text_color", "text", "placeholder", "autocorrection_type",
             "spellchecking_type", "secure", "editable", "image_name",
             "font_bold", "action", "continuous", "value", "segments", "title",
             "scales_to_fit", "row_height", "editing", "data_source_items",
             "data_source_action", "data_source_edit_action",
             "data_source_accessory_action", "data_source_font_size",
             "data_source_move_enabled", "data_source_number_of_lines", "mode",
             "content_width", "content_height", ("image", "image_name")]
    # Tuples are used to indicate when an attribute has a different name in the
    # pyui file than it does in an actual object. We convert everything to a
    # tuple for convenience.
    attrs = [a if isinstance(a, tuple) else (a,) * 2 for a in attrs]

    # This is mostly robust, though there are a few edge cases
    for attr_name in attrs:
        if hasattr(view, attr_name[0]):
            attr = getattr(view, attr_name[0])
            if not isinstance(attr, (int, float, bool, str, type(None))):
                attr = str(attr)
            if attr_name not in out["attributes"] and attr not in (None, ""):
                out["attributes"][attr_name[1]] = attr

    return out


def dump_view(view, path):
    """ The reverse of `ui.load_view()`"""
    with open(path, "w") as f:
        json.dump(view_to_dict(view), f)


if __name__ == "__main__":
    import ui
    a = ui.Button()
    a.title = "Hey, it's a thing!"
    b = ui._view_from_dict(view_to_dict(a), globals(), locals())
    assert b.title == "Hey, it's a thing!"
