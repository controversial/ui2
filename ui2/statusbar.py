from objc_util import *
from ui import parse_color

app = UIApplication.sharedApplication()
rootvc = app.keyWindow().rootViewController()


def set_color(color):
    """Change the text color of the status bar."""
    if color not in (0, 1):
        raise ValueError("Color must be 0 (black) or 1 (white)")
    rootvc.setStatusBarStyle_(color)
    rootvc.setNeedsStatusBarAppearanceUpdate()


def set_visibility(should_show):
    """Can't get this to work no matter what..."""
    raise NotImplementedError()
