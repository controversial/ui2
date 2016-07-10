from objc_util import *


CATransaction = ObjCClass("CATransaction")


def animate(animation, duration=0.25, delay=0.0, completion=None):
    """A drop-in replacement for ui.animate which supports easings."""
    if completion is not None:
        completion = ObjCBlock(completion, argtypes=[c_bool])

    UIView.animateWithDuration_delay_options_animations_completion_(
        duration,
        delay,
        0,  # No options
        ObjCBlock(animation),
        completion
    )

if __name__ == "__main__":
    import ui
    v = ui.View()
    v.width = v.height = 500

    b = ui.View()
    b.width = b.height = b.x = b.y = 100
    b.background_color = "white"

    v.add_subview(b)

    def a():
        b.x = 300

    def completion(success):
        print(success)

    v.present("sheet")

    animate(a, 0.25, 0.25)
