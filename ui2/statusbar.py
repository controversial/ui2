from objc_util import *
from ui import parse_color

app = UIApplication.sharedApplication()
rootvc = app.keyWindow().rootViewController()

class StatusBar(object):
    """The system status bar."""

    status = app.statusBar()

    # Color

    @property
    def color(self):
        """Get the color of the status bar.
        
        0 is black, 1 is white.
        """
        return rootvc.statusBarStyle()

    @color.setter
    def color(self, color):
        """Change the text color of the status bar."""
        if color not in (0, 1):
            raise ValueError("Color must be 0 (black) or 1 (white)")
        rootvc.setStatusBarStyle_(color)
        rootvc.setNeedsStatusBarAppearanceUpdate()

    # Background color

    @property
    def background_color(self):
        if self.status.backgroundColor() == None:
            return (0.0, 0.0, 0.0, 0.0)
        else:
            color = self.status.backgroundColor()
            return color.red(), color.green(), color.blue(), color.alpha()

    @background_color.setter
    def background_color(self, color):
        rgba = parse_color(color)
        self.status.setBackgroundColor_(
            UIColor.colorWithRed_green_blue_alpha_(*rgba)
        )

    # Visibility

    def _set_visibility(self, should_show):
        """Hide or show the status bar."""
        self.status.hidden = not should_show
    
    @property
    def is_visible(self):
        return not self.status.isHidden( )

    def hide(self):
        """Hide the status bar."""
        self._set_visibility(False)
    
    def show(self):
        """Show the status bar."""
        self._set_visibility(True)

    def toggle(self):
        """Toggle the status bar."""
        self._set_visibility(False if self.is_visible else True)

    # Other

    def reset(self):
        self.background_color = "clear"
        self.color = 1
        self.show()

# The only instance ever needed. There's no point in having multiple. StatusBar
# is only a class so that "@property"s can be used.
statusbar = StatusBar()
