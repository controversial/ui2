"""A submodule for helping to "subclass" ui.View objects."""

import ui
from ui2.subclassing import proxies


class ViewClassProxy(proxies.TypeProxy, ui.View):
    """A complete ui.View proxy, almost indistinguishible from the view it
    wraps.

    This essentially works by encapsulating the uninheritable view in a
    container view. The container is its own view, but it's transparent, and
    all access to this object is delegated to the wrapped view. So although the
    ViewClassProxy is its own view with its own properties, thse attributes
    can't be easily accessed, all access is forwarded to the contained view.

    For example, trying to access a ViewClassProxy's 'frame' will transparently
    return the contained view's frame instead, and setting it will leave the
    ViewClassProxy's frame untouched while instead modifying the contained
    view's frame.
    """

    def __init__(self, view_type, *args, **kwargs):
        super().__init__(view_type, *args, **kwargs)
        # Add subject as a subview
        object.__getattribute__(self, "add_subview")(self.__subject__)
        # Allow flexible width and height so that this view fills its entire
        # container.
        object.__setattr__(self, "flex", "WH")


class ViewClassWrapper(ViewClassProxy, proxies.AbstractWrapper):
    """A complete ui.View proxy, almost indistinguishible from the view it
    wraps. See ViewClassProxy for details."""
    pass


def subclassable(view_type):
    """Return an inheritable version of an uninheritable ui.View class."""
    class ViewWrapper(ViewClassWrapper):
        def __init__(self, *args, **kwargs):
            super().__init__(view_type, *args, **kwargs)
    return ViewWrapper
