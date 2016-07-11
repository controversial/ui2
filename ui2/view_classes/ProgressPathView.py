from objc_util import *
import ui


def _get_CGColor(color):
    """Get a CGColor from a wide range of formats."""
    return UIColor.colorWithRed_green_blue_alpha_(
        *ui.parse_color(color)
    ).CGColor()


class ProgressPathView(ui.View):
    """A view class which can turn a ui.Path into a progress bar.

    This allows you not only to create linear and circular progress bars, but
    to create progress bars of any shape """
    def __init__(self, path, width=5, color="#21abed",
                 show_track=True, track_width=5, track_color="#eee"):

        # Draw the full path on one layer
        self._track_layer = ObjCClass("CAShapeLayer").new()
        self._track_layer.setFillColor_(UIColor.clearColor().CGColor())
        self._track_layer.setStrokeColor_(_get_CGColor(track_color))
        self._track_layer.setLineWidth_(track_width)
        self._track_layer.setPath_(ObjCInstance(path).CGPath())
        ObjCInstance(self).layer().addSublayer_(self._track_layer)
        # Set up the layer on which the partial path is rendered
        self._layer = ObjCClass("CAShapeLayer").new()
        self._layer.setFillColor_(UIColor.clearColor().CGColor())  # No fill
        self._layer.setPath_(ObjCInstance(path).CGPath())
        ObjCInstance(self).layer().addSublayer_(self._layer)

        self.progress = 0  # Progress starts at 0

        # Apply arguments
        self.color = color
        self.stroke_width = width

        self.track_color = track_color
        self.track_width = track_width
        
        if not show_track:
            self._track_layer.setOpacity_(0)


    # Update progress level

    @property
    def progress(self):
        return self._layer.strokeEnd()

    @progress.setter
    def progress(self, value):
        self._layer.setStrokeEnd_(value)
        self._layer.setNeedsDisplay()

    # Progress bar

    @property
    def stroke_width(self):
        return self._layer.lineWidth()

    @stroke_width.setter
    def stroke_width(self, width):
        self._layer.setLineWidth_(width)

    @property
    def color(self):
        color = UIColor.colorWithCGColor_(self._layer.strokeColor())
        return color.red(), color.green(), color.blue(), color.alpha()

    @color.setter
    def color(self, color):
        self._layer.setStrokeColor_(_get_CGColor(color))

    # Track

    @property
    def track_color(self):
        color = UIColor.colorWithCGColor_(self._track_layer.strokeColor())
        return color.red(), color.green(), color.blue(), color.alpha()

    @track_color.setter
    def track_color(self, color):
        self._track_layer.setStrokeColor_(_get_CGColor(color))

    @property
    def track_width(self):
        return self._track_layer.lineWidth()

    @track_width.setter
    def track_width(self, width):
        self._track_layer.setLineWidth_(width)

    @property
    def track_shown(self):
        return bool(self._track_layer.opacity())

    def show_track(self):
        """Show the progress bar track."""
        self._track_layer.setOpacity_(1)
    
    def hide_track(self):
        """Hide the progress bar track."""
        self._track_layer.setOpacity_(0)
    
    def toggle_track(self):
        """Toggle the visibility of the track."""
        self._track_layer.setOpacity_(0 if self.track_shown else 1)

    # Extras

    @property
    def is_complete(self):
        return self.progress == 1

    def complete(self):
        """Finish the progressbar."""
        self.progress = 1
