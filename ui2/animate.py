from objc_util import *


def animate(animation, duration=0.25, delay=0.0, completion=None):
    """A drop-in replacement for ui.animate which supports easings."""
    if completion is not None:
        def c(cmd, success):
            completion(success)
            release_global(ObjCInstance(cmd))
        oncomplete = ObjCBlock(c, argtypes=[c_void_p, c_void_p])
        retain_global(oncomplete)
    else:
        oncomplete = None

    UIView.animateWithDuration_delay_options_animations_completion_(
        duration, delay, 0, ObjCBlock(animation), oncomplete
    )
