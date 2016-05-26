"""
Easily draw different shapes and polygons using Pythonista's UI module. Also
includes methods for storing these shapes as JSON.
"""

from math import sin, cos, pi

import ui


# HELPER METHODS

def _polar2cart(radius, theta):
    """ Convert polar coordinates to cartesian coordinates """
    theta = theta / (180 / pi)  # Degrees to radians
    return (radius * cos(theta), radius * sin(theta))


# MAIN METHODS

def draw_polygon(points, color="#000"):
    """ Draw an enclosed polygon given a list of points that form the shape """

    ui.set_color(color)
    p = ui.Path()
    # Move to first point
    p.move_to(*points[0])
    # Begin path, drawing line to the rest
    for point in points[1:]:
        p.line_to(*point)
    # Go back to start to close the shape
    p.close()
    # Fill with color
    p.fill()


def draw_regular_polygon(n, center, radius, rotation=0, color="#000"):
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
    draw_polygon(points, color)
