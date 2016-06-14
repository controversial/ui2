import objc_util
import ui


# We can't inherit :(
class Path():
    """ A magical wrapper around ui.Path that allows you to track where the
    path goes. Tracks all the points in the path, as well as the exact
    parameters used to create each component of the path """
    def __init__(self):
        self.p = ui.Path()

        # Stores all arcs, curves, and lines in the path. They are stored as
        # [start_point, function_args, end_point]
        self.components = []
        # Keeps track of the current position internally. Only updated manually
        # and is therefore used to track old values
        self._position = (0, 0)

        # Copy docstring
        self.__doc__ == ui.Path.__doc__

    # Wrapper methods

    def move_to(self, x, y):
        # Not stored in components, since it isn't part of the path. Can be
        # easily inferred from gaps between one ending position and the next
        # initial position, however
        self.p.move_to(x, y)
        self._position = x, y

    def line_to(self, x, y):
        self.p.line_to(x, y)
        self.components.append(
            [self._position,  # Initial position
             (x, y),          # Arguments passed
             self.position,   # Ending position
             "line_to"]       # Method used
        )
        self._position = self.position

    def add_arc(self, center_x, center_y, radius, start_angle, end_angle):
        self.p.add_arc(center_x, center_y, radius, start_angle, end_angle)
        self.components.append(
            [self._position,                                        # Initial
             (center_x, center_y, radius, start_angle, end_angle),  # Args
             self.position,                                         # Ending
             "add_arc"]                                             # Method
        )
        self._position = self.position

    def add_curve(self, end_x, end_y, cp1_x, cp1_y, cp2_x, cp2_y):
        self.p.add_curve(end_x, end_y, cp1_x, cp1_y, cp2_x, cp2_y)
        self.components.append(
            [self._position,                              # Initial position
             (end_x, end_y, cp1_x, cp1_y, cp2_x, cp2_y),  # Arguments passed
             self.position,                               # Ending position
             "add_curve"]                                 # Method used
        )
        self._position = self.position

    def add_quad_curve(self, end_x, end_y, cp_x, cp_y):
        self.p.add_quad_curve(end_x, end_y, cp_x, cp_y)
        self.components.append(
            [self._position               # Initial position
             (end_x, end_y, cp_x, cp_y),  # Arguments passed
             self.position,               # Ending position
             "add_quad_curve"]            # Method used
        )

    def append_path(other_path):
        raise NotImplementedError()

    def close(self):
        self.p.close()
        self.components.append(
            [self._position,  # Initial position
             (),              # Aruments passed
             self.position,   # Ending position
             "close"]         # Method used
        )

    # Extended API (besides what's in __init__)

    @property
    def position(self):
        """ Current position """
        pos = objc_util.ObjCInstance(self.p).currentPoint()
        return pos.x, pos.y

    @property
    def points(self):
        return [c[0] for c in self.components]

    @property
    def is_closed(self):
        return self.components[-1][2] == self.components[0][0]

    # Allow transparant access to the ui.path items

    def __getattr__(self, key):
        return getattr(self.p, key)

if __name__ == "__main__":
    with ui.ImageContext(100, 100) as ctx:
        a = Path()
        # Tests
        a.move_to(10, 10)
        a.line_to(20, 20)
        a.line_to(20, 50)
        a.line_to(50, 10)
        print(a.points)
        a.close()
        a.fill()
        ctx.get_image().show()
