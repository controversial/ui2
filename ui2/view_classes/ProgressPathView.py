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
    def __init__(self, path, width=5, color="#21abed"):
        self._objc = ObjCInstance(self)
        # Set up the layer on which the path is rendered
        self._layer = ObjCClass("CAShapeLayer").new()
        self._layer.setPath_(ObjCInstance(path).CGPath())
        self._objc.layer().addSublayer_(self._layer)

        self._layer.setFillColor_(UIColor.clearColor().CGColor())  # No fill
        self.tint_color = color

        self.stroke_width = width
        self.progress = 0  # Progress starts at 0
    
    @property
    def progress(self):
        return self._layer.strokeEnd()
    
    @progress.setter
    def progress(self, value):
        self._layer.setStrokeEnd_(value)

    @property
    def stroke_width(self):
        return self._layer.lineWidth()
    
    @stroke_width.setter
    def stroke_width(self, width):
        self._layer.setLineWidth_(width)
    
    @property
    def tint_color(self):
        color = UIColor.colorWithCGColor_(self._layer.strokeColor())
        return color.red(), color.green(), color.blue(), color.alpha()
    
    @tint_color.setter
    def tint_color(self, color):
        self._layer.setStrokeColor_(_get_CGColor(color))


if __name__ == "__main__":
    p = ui.Path()
    p.move_to(10, 10)
    p.line_to(50, 10)
    p.line_to(50, 50)
    p.close()
    
    a = ProgressPathView(p)
    b = ui.View()
    b.add_subview(a)

    b.present("sheet")
    
    a.progress = 0.1
    def advance():
        a.progress = 0.7
    ui.delay(advance, 0.75)
    def advance2():
        a.progress = 1
    ui.delay(advance2, 1.5)
