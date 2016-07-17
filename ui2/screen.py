"""Class for screen sizes and orientation."""
import objc_util
import ui


app = objc_util.UIApplication.sharedApplication()
UIScreen = objc_util.ObjCClass("UIScreen")

orientation_codes = {
    1: "bottom",
    2: "top",
    3: "left",
    4: "right"
}


class _ScreenOrientation(object):
    """Represents a device orientation state."""
    def __init__(self, orientation):
        self.code = orientation

    def __str__(self):
        return orientation_codes[self.code]

    @property
    def portrait(self):
        return self.code in (1, 3)
    
    @property
    def landscape(self):
        return self.code in (2, 4)


class Screen(object):
    """An interface to access characteristics of the device's screen."""
    @property
    def size(self):
        """Get screen size."""
        return ui.get_screen_size()
    
    @property
    def width(self):
        """The width of the screen."""
        return self.size[0]

    @property
    def height(self):
        """The height of the screen."""
        return self.size[1]

    @property
    def min(self):
        return min(self.size)

    @property
    def max(self):
        return max(self.size)

    def __iter__(self):
        """This allows the min and max functions to work on this class."""
        return iter(self.size)

    @property
    def orientation(self):
        """Get a numerical value representing the screen's orientation."""
        # This doesn't use UIDevice because my approach is simpler, and
        # accounts for rotation lock automatically.
        return _ScreenOrientation(app.statusBarOrientation())

    @property
    def portrait(self):
        return self.orientation.portrait
    
    @property
    def landscape(self):
        return self.orientation.landscape

    @property
    def is_retina(self):
        return UIScreen.mainScreen().scale() == 2.0

screen = Screen()
