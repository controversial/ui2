"""
Easily draw different shapes and polygons using Pythonista's UI module.
"""

from math import sin, cos, pi

import ui
import ui2


# HELPER METHODS

def _polar2cart(radius, theta):
    """ Convert polar coordinates to cartesian coordinates """
    theta = theta / (180 / pi)  # Degrees to radians
    return (radius * cos(theta), radius * sin(theta))


# MAIN METHODS

def get_polygon_path(points):
    """ Get a ui.Path object that connects a list of points with straight lines
    to form a closed figure """
    p = ui.Path()
    # Move to first point
    p.move_to(*points[0])
    # Begin path, drawing line to the rest
    for point in points[1:]:
        p.line_to(*point)
    # close the shape
    p.close()

    return p


def get_regular_polygon_points(n, center=(20, 20), radius=20, rotation=0):
    """ Get the points to form a regular polygon given the number of sides, the
    center, the radius. The polygon will be drawn so that the base is flat
    horizontal, unless `rotation` is specified, in which case the polygon will
    be rotated by `rotation` degrees clockwise from the original """
    if n < 3:
        raise ValueError("A polygon must have at least 3 points")
    # Adjust for flat bottom, then add 90 because 0 is straight right in the
    # standard polar coordinate system
    rotation += 360.0 / n / 2 + 90
    # The polar coordinate values of theta at which the points go
    degree_intervals = [360.0 / n * i + rotation for i in range(n)]
    # The cartesian coordinates where the points go
    points = [_polar2cart(radius, theta) for theta in degree_intervals]
    points = [(center[0] + p[0], center[1] + p[1]) for p in points]

    return points


def get_regular_polygon_path(*args, **kwargs):
    """ Get a ui.Path for a regular polygon. See 'get_regular_polygon_points'
    for description of arguments """
    return get_polygon_path(get_regular_polygon_points(*args, **kwargs))


def draw_shape_from_dict():
    """ Draw a shape from a dict, as it is stored in .pyui2 files """
    raise NotImplementedError()


# VIEW CLASSES

class PathView(ui.View):
    """ A class for displaying a ui.Path inside a ui.View, which automatically
    scales and moves the path when you change the frame """
    def __init__(self, path, color="black", shadow=("black", 0, 0, 0)):
        # Store arguments
        self._path = path
        self._color = color
        self._shadow = shadow
        # Store other data (data that requires processing)
        self._pathsize = path.bounds.max_x, path.bounds.max_y
        self.width, self.height = self._pathsize

    def draw(self):
        # Set drawing attributes
        ui.set_color(self._color)
        ui.set_shadow(*self._shadow)
        # Calculations
        scale_x = self.width / self._pathsize[0]
        scale_y = self.height / self._pathsize[0]
        # Scale the path
        new_path = ui2.path_helpers.scale_path(self._path, (scale_x, scale_y))
        new_path.fill()


if __name__ == "__main__":
    # SETUP
    p = get_regular_polygon_path(6, center=(50, 50), radius=50)
    pv = PathView(p)
    pv.x = 150
    pv.y = 150
    ui2.path_helpers.get_path_image(p).show()

    # ANIMATION FUNCTIONS
    def scaleWidth():
        pv.width = 200

    def scaleHeight():
        pv.height = 200

    def scaleBoth():
        pv.width = 300
        pv.height = 300

    def scaleBack():
        pv.x, pv.y = 0, 0
        pv.width, pv.height = 50, 50

    # BASIC USAGE
    v = ui.View()
    v.width, v.height = 500, 500
    v.add_subview(pv)
    v.present("sheet")
    # PERFORM THE ANIMATIONS
    ui.animate(scaleWidth, 1)
    ui.delay(lambda: ui.animate(scaleHeight, 1), 1)
    ui.delay(lambda: ui.animate(scaleBoth, 1), 2)
    ui.delay(lambda: ui.animate(scaleBack, 1), 3)
