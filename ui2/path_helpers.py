import ui


def get_path_image(path):
    """ Get an image of a path """
    bounds = path.bounds
    with ui.ImageContext(bounds.max_x, bounds.max_y) as ctx:
        path.fill()
        return ctx.get_image()
