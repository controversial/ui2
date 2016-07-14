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


class Transition(object):
    """Represents a transition between two views."""
    def __init__(self, view1, view2, effect=TRANSITION_FLIP_FROM_RIGHT,
                 duration=0.25, completion=None):
        self.view1 = view1
        self.view2 = view2
        self.effect = effect
        self.duration = duration
        self.completion = completion

    def play(self):
        """Perform the transition."""
        # Make frames match, it's way cleaner.
        self.view2.frame = self.view1.frame

        # Fix for early garbage-collection of completion function
        if self.completion is not None:
            def c(cmd, success):
                    self.completion(success)
                    release_global(ObjCInstance(cmd))
            oncomplete = ObjCBlock(c, argtypes=[c_void_p, c_bool])
            retain_global(oncomplete)
        else:
            oncomplete = None
        # Perform the transition
        UIView.transitionFromView_toView_duration_options_completion_(
            self.view1, self.view2, self.duration, self.effect, oncomplete
        )


class ChainedTransitionComponent(Transition):
    def __init__(self, transition_obj, next_transition):
        """A single step in a chain of transitions."""
        self.transition_obj = transition_obj
        self.next_transition = next_transition

        self.view1 = self.transition_obj.view1
        self.view2 = self.transition_obj.view2
        self.effect = self.transition_obj.effect
        self.duration = self.transition_obj.duration

    def completion(self, success):
        # If it has a completion function already, run it first.
        if self.transition_obj.completion is not None:
            self.transition_obj.completion(success)
        # Then play the next transition if we're not at the end of the chain
        if self.next_transition is not None:
            self.next_transition.play()


class ChainedTransition(object):
    """Represents a series of several transitions to be played in sequence."""
    def __init__(self, *transitions):
        transits = []
        for i, a in reversed(list(enumerate(transitions))):
            if i == len(transitions) - 1:
                # This is the last element in the chain (first in iteration),
                # so it has no successor. We can use the old Animation object.
                transits.append(a)
            else:
                transits.append(ChainedTransitionComponent(a, transits[-1]))

        self.transitions = transits[::-1]

    def play(self):
        """Perform the transitions."""
        self.transitions[0].play()


def transition(*args, **kwargs):
    """Transition from one view to another."""
    Transition(*args, **kwargs).play()
