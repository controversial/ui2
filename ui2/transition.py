from objc_util import *

# Constants
TRANSITION_NONE = 0 << 20
TRANSITION_FLIP_FROM_TOP = 6 << 20
TRANSITION_FLIP_FROM_RIGHT = 2 << 20
TRANSITION_FLIP_FROM_BOTTOM = 7 << 20
TRANSITION_FLIP_FROM_LEFT = 1 << 20
TRANSITION_CURL_UP = 3 << 20
TRANSITION_CURL_DOWN = 4 << 20
TRANSITION_CROSS_DISSOLVE = 5 << 20


def transition(from_view, to_view,
               effect=TRANSITION_NONE, duration=1, completion=None):
    """Transition from one view to another."""
    # Fix for presentation with show_title_bar=True
    if from_view.y == 44:
        to_view.y = 44

    # Fix for early garbage-collection of completion function
    if completion is not None:
        def c(cmd, success):
                completion(success)
                release_global(ObjCInstance(cmd))
        oncomplete = ObjCBlock(c, argtypes=[c_void_p, c_bool])
        retain_global(oncomplete)
    else:
        oncomplete = None

    # Perform the transition
    UIView.transitionFromView_toView_duration_options_completion_(
        from_view, to_view, duration, effect, oncomplete
    )
