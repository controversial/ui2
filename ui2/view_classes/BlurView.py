from objc_util import *
import ui


class BlurView(ui.View):
    """A class for applying a heavy iOS-style blur to elements behind it."""
    def __init__(self, dark=False, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

        self._objc = ObjCInstance(self)
        self.background_color = 'clear'
        self._effect_view = ObjCClass('UIVisualEffectView').new()
        self._effect_view.setFrame_(self._objc.frame())
        # Flexible width and height
        self._effect_view.setAutoresizingMask_((1 << 1) + (1 << 4))

        self._set_dark(dark)
        self._objc.addSubview_(self._effect_view)

    @on_main_thread
    def _set_dark(self, dark=True):
        """Set whether the blur is dark or light."""
        style = 2 if dark else 1
        self._effect = ObjCClass('UIBlurEffect').effectWithStyle(style)
        self._effect_view.setEffect_(self._effect)

    @property
    def dark(self):
        return True if self._effect._style() == 2 else False

    @dark.setter
    def dark(self, value):
        self._set_dark(value)

    @property
    def light(self):
        return not self.dark

    @light.setter
    def light(self, value):
        self.dark = not value

    def toggle_brightness(self):
        """Toggle the view's brightness between light and dark."""
        self.dark = not self.dark
