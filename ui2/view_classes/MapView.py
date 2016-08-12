import objc_util
import ui


# CTYPES


class _CoordinateRegion (objc_util.Structure):
    _fields_ = [
        ("center", objc_util.CGPoint),
        ("span", objc_util.CGSize)
    ]


# MAIN INTERFACE


class MapView(ui.View):
    @objc_util.on_main_thread
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

        self._view = objc_util.ObjCClass("MKMapView").new()
        self._view.setFrame_(
            objc_util.CGRect(
                objc_util.CGPoint(0, 0),
                objc_util.CGSize(self.width, self.height)
            )
        )
        self._view.setAutoresizingMask_(18)  # W+H
        objc_util.ObjCInstance(self).addSubview_(self._view)

        self.animated = True

    @property
    def bounds(self):
        """The upper left and lower right coordinates of the visible map area
        as latitude/longitude values."""
        center = self._view.region().a.a, self._view.region().a.b
        span = self._view.region().b.a, self._view.region().b.b
        min_x = center[0] - span[0] / 2
        min_y = center[1] - span[1] / 2
        max_x = center[0] + span[0] / 2
        max_y = center[1] + span[1] / 2

        return min_x, min_y, max_x, max_y

    @bounds.setter
    def bounds(self, coords):
        """get the upper left and lower right coordinates of the visible map
        area with latitude/longitude values."""
        topleft, bottomright = coords[:2], coords[2:]

        min_x, min_y = topleft
        max_x, max_y = bottomright
        span = (
            max_x - min_x,
            max_y - min_y
        )
        center = (
            min_x + span[0] / 2,
            min_y + span[1] / 2
        )
        self._view.setRegion_animated_(
            _CoordinateRegion(
                objc_util.CGPoint(*center),
                objc_util.CGSize(*span),
            ),
            self.animated,

            restype=None, argtypes=[_CoordinateRegion, objc_util.c_bool]
        )

    @property
    def center(self):
        coord = self._view.centerCoordinate()
        return coord.a, coord.b

    @center.setter
    def center(self, coords):
        self._view.setCenterCoordinate_animated_(
            objc_util.CGPoint(coords[0], coords[1]),
            self.animated,
            restype=None,
            argtypes=[objc_util.CGPoint, objc_util.c_bool]
        )
