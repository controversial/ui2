import ui
import ui2


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
