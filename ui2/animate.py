import warnings

from objc_util import *


# Constants representing easings. See http://apple.co/29FOF5i

ANIMATE_EASE_IN = 1 << 16
ANIMATE_EASE_OUT = 2 << 16
ANIMATE_EASE_IN_OUT = 0 << 16
ANIMATE_EASE_NONE = ANIMATE_LINEAR = 3 << 16


class Animation(object):
    """Represents an animation to one or more properties of an object."""
    def __init__(self, animation, duration=0.25, delay=0.0, completion=None,
                 easing=ANIMATE_EASE_IN_OUT):
        self.animation = animation
        self.duration = duration
        self.delay = delay
        self.completion = completion
        self.easing = easing

    def play(self):
        """Perform the animation."""
        if self.completion is not None:
            def c(cmd, success):
                self.completion(success)
                release_global(ObjCInstance(cmd))
            oncomplete = ObjCBlock(c, argtypes=[c_void_p, c_bool])
            retain_global(oncomplete)
        else:
            oncomplete = None

        UIView.animateWithDuration_delay_options_animations_completion_(
            self.duration,
            self.delay,
            self.easing,
            ObjCBlock(self.animation),
            oncomplete
        )


class ChainedAnimationComponent(Animation):
    def __init__(self, animation_obj, next_animation):
        """A single step in a chain of animations."""
        self.animation_obj = animation_obj
        self.next_animation = next_animation

        self.duration = self.animation_obj.duration
        self.delay = self.animation_obj.delay
        self.animation = self.animation_obj.animation
        self.easing = self.animation_obj.easing

    def completion(self, success):
        self.animation_obj.completion(success)
        if self.next_animation is not None:
            self.next_animation.play()


class ChainedAnimation(object):
    """Represents a series of several animations to be played in sequence."""
    def __init__(self, *animations):
        self.anims = [ChainedAnimationComponent(
                      a,
                      animations[i + 1] if i < len(animations) - 1 else None
                      ) for i, a in enumerate(animations)]

    def play(self):
        """Perform the animations."""
        self.anims[0].play()


def animate(animation, *args, **kwargs):
    """A drop-in replacement for ui.animate.

    This adds support for different easings.
    """
    Animation(animation, *args, **kwargs).play()
