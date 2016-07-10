import warnings

from objc_util import *


# Basic animation class

class Animation(object):
    """Represents an animation to one or more properties of an object"""
    def __init__(self, animation, duration=0.25, delay=0.0, completion=None):
        self.animation = animation
        self.duration = duration
        self.delay = delay
        self.completion = completion

    def play(self):
        """Perform the animation"""
        if self.completion is not None:
            def c(cmd, success):
                self.completion(success)
                print("Ran completion object")
                release_global(ObjCInstance(cmd))
            oncomplete = ObjCBlock(c, argtypes=[c_void_p, c_bool])
            retain_global(oncomplete)
        else:
            oncomplete = None

        UIView.animateWithDuration_delay_options_animations_completion_(
            self.duration, self.delay, 0, ObjCBlock(self.animation), oncomplete
        )


def animate(animation, duration=0.25, delay=0.0, completion=None):
    """A drop-in replacement for ui.animate"""
    Animation(animation, duration, delay, completion).play()
