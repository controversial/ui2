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
                release_global(ObjCInstance(cmd))
            oncomplete = ObjCBlock(c, argtypes=[c_void_p, c_bool])
            retain_global(oncomplete)
        else:
            oncomplete = None

        UIView.animateWithDuration_delay_options_animations_completion_(
            self.duration, self.delay, 0, ObjCBlock(self.animation), oncomplete
        )


class ChainedAnimationComponent(Animation):
    def __init__(self, animation, next_animation):
        self.animation_obj = animation
        self.next_animation = next_animation

        self.duration = self.animation_obj.duration
        self.delay = self.animation_obj.delay
        self.animation = self.animation_obj.animation

    def completion(self, success):
        self.animation_obj.completion(success)
        if self.next_animation is not None:
            self.next_animation.play()


class ChainedAnimation(object):
    def __init__(self, *animations):
        self.anims = [ChainedAnimationComponent(
                      a,
                      animations[i + 1] if i < len(animations) - 1 else None
                      ) for i, a in enumerate(animations)]

    def play(self):
        self.anims[0].play()


def animate(animation, duration=0.25, delay=0.0, completion=None):
    """A drop-in replacement for ui.animate"""
    Animation(animation, duration, delay, completion).play()
