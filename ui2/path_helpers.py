import ui
import objc_util


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


def scale_path(path, scale):
    """ Stretch or scale a path. Pass either a scale or a tuple of scales """
    if not hasattr(scale, "__iter__"):
        scale = (scale, scale)
    sx, sy = scale

    newpath = copy_path(path)
    # Construct an affine transformation matrix
    transform = objc_util.CGAffineTransform(sx, 0, 0, sy, 0, 0)
    # Apply it to the path
    objcpath = objc_util.ObjCInstance(newpath)
    objcpath.applyTransform_(transform)
    return newpath
