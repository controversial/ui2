"""
Easily draw different shapes and polygons using Pythonista's UI module.
"""

from math import sin, cos, pi

import ui


# HELPER METHODS

def _polar2cart(radius, theta):
    """ Convert polar coordinates to cartesian coordinates """
    theta = theta / (180 / pi)  # Degrees to radians
    return (radius * cos(theta), radius * sin(theta))


# MAIN METHODS

def draw_polygon(points):
    """ Draw an enclosed polygon given a list of points that form the shape.
    Obeys the ui.GState for settings like color, shadow, etc. """

    p = ui.Path()
    # Move to first point
    p.move_to(*points[0])
    # Begin path, drawing line to the rest
    for point in points[1:]:
        p.line_to(*point)
    # Go back to start to close the shape
    p.close()
    # Fill
    p.fill()


def draw_regular_polygon(n, center, radius, rotation=0):
    """ Draw a regular polygon given the number of sides, the center, the
    radius. The polygon will be drawn so that the base is flat horizontal,
    unless `rotation` is specified, in which case the polygon will be rotated
    by `rotation` degrees clockwise from the original """

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
    # Draw the polygon
    draw_polygon(points)

    return points


def draw_shape_from_dict():
    """ Draw a shape from a dict, as it is stored in .pyui2 files """
    pass


# VIEW CLASSES

class Polygon(ui.View):
    """ A Polygon that you can add to a ui.View as a subview.
    Scaling is *not* currently implemented. Eventually, adjusting the width and
    height will automatically adjust the position of the points """
    def __init__(self, points, color="#000", shadow=("#000", 0, 0, 0)):
        self.points = points
        self.color = color
        self.shadow = shadow

        super(Polygon, self).__init__(self)

    def draw(self):
        ui.set_shadow(*self.shadow)
        ui.set_color(self.color)

        draw_polygon(self.points)


class RegularPolygon(ui.View):
    def __init__(self, n, rotation=0, color="#000", shadow=("#000", 0, 0, 0)):
        self.num_sides = n
        self.rotation = rotation
        self.color = color
        self.shadow = shadow

        super(RegularPolygon, self).__init__(self)

    def draw(self):
        ui.set_shadow(*self.shadow)
        ui.set_color(self.color)

        draw_regular_polygon(self.num_sides, (self.width / 2, self.height / 2),
                             min(self.width, self.height) / 3, self.rotation)

if __name__ == "__main__":
    # BASIC USAGE
    v = ui.View()
    p = RegularPolygon(5, color="#333", shadow=("#0cf", 10, 10, 5))
    v.add_subview(p)

    # Miscellaneous
    v.background_color = "#fff"
    v.width, v.height = ui.get_screen_size()

    v.present()

    # FANCY ANIMATIONS
    # Note that this isn't really necessary, basic usage is what is above. All
    # this code is just to animate changing position and size
    def move():
        p.x, p.y = v.width - p.width, v.height - p.height
    ui.animate(move, 1)

    def moveBack():
        p.x, p.y = 0, 0
    ui.delay(lambda: ui.animate(moveBack, 1), 1)

    def scale():
        size = min(v.width, v.height)
        p.width, p.height = size, size

    ui.delay(lambda: ui.animate(scale, 1), 2)

    def scaleBack():
        p.width, p.height = 100, 100
    ui.delay(lambda: ui.animate(scaleBack, 1), 4)
