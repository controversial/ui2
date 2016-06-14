import ui


def get_path_image(path):
    """ Get an image of a path """
    bounds = path.bounds
    with ui.ImageContext(bounds.max_x, bounds.max_y) as ctx:
        path.fill()
        return ctx.get_image()


def copy_path(path):
    """ Make a copy of a ui.Path and return it. Preserves all data. """
    new = ui.Path()
    new.append_path(path)
    # Copy over the attributes
    new.line_cap_style = path.line_cap_style
    new.line_join_style = path.line_join_style
    new.line_width = path.line_width

    return new
