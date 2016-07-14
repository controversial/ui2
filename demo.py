import ui
import ui2


# DEMOS -----------------------------------------------------------------------


def demo_PathView():
    # SETUP
    p = ui2.get_regular_polygon_path(6, center=(50, 50), radius=50)
    pv = ui2.PathView(p)
    pv.x = 150
    pv.y = 150
    # ANIMATION FUNCTIONS
    def scaleWidth():
        pv.width = 200
    def scaleHeight():
        pv.height = 200
    def scaleBoth():
        pv.width = 300
        pv.height = 300
    def scaleBack():
        pv.x, pv.y = 0, 0
        pv.width, pv.height = 50, 50
    # BASIC USAGE
    v = ui.View()
    v.width = v.height = 500
    v.add_subview(pv)
    v.present("sheet")
    # PERFORM THE ANIMATIONS
    ui.animate(scaleWidth, 1)
    ui.delay(lambda: ui.animate(scaleHeight, 1), 1)
    ui.delay(lambda: ui.animate(scaleBoth, 1), 2)
    ui.delay(lambda: ui.animate(scaleBack, 1), 3)


def demo_Polygon():
    for i in range(3, 9):  # Triangle to octagon
        p = ui2.get_regular_polygon_path(i, center=(50, 50), radius=50)
        ui2.pathutil.get_path_image(p).show()


def demo_ProgressPathView():
    import math
    import random

    p = ui.Path()
    p.move_to(20, 20)
    p.line_to(480, 20)
    p.line_to(480, 250)
    p.add_arc(250, 250, 230, 0, math.radians(110))
    p.add_curve(50, 450, 20, 250, 480, 250)
    p.close()  # This makes the end look nicer

    ppv = ui2.ProgressPathView(p, color="red")

    view = ui.View()
    view.add_subview(ppv)
    view.width = view.height = ppv.width = ppv.height = 500
    view.present("sheet")

    def advance():
        """Advance by a random amount and repeat."""
        pg = ppv.progress + random.random() / 20
        if pg < 1:
            ppv.progress = pg
            ui.delay(advance, random.random() / 2)
        else:
            ppv.progress = 1

    advance()


def demo_Animation():
    v = ui.View()
    v.width = v.height = 500
    v.background_color = "red"

    b = ui.View()
    b.width = b.height = b.x = 100
    b.y = 200
    b.background_color = "white"

    v.add_subview(b)

    def a():
        b.x = 300

    def completion(success):
        print("Done!")

    v.present("sheet", hide_title_bar=True)

    ui2.animate(a, 0.25, 0.25, completion)


def demo_ChainedAnimation():
    v = ui.View()
    v.width = v.height = 500
    v.background_color = "red"

    b = ui.View()
    b.width = b.height = b.x = 100
    b.y = 200
    b.background_color = "white"

    v.add_subview(b)

    def animation_a():
        print("Animating...")
        b.x = 300

    def animation_b():
        b.x = 100

    def completion(success):
        print("Done!")

    a_anim = ui2.Animation(animation_a, 1, easing=ui2.ANIMATE_EASE_IN)
    b_anim = ui2.Animation(animation_b, 1, easing=ui2.ANIMATE_EASE_OUT)

    v.present("sheet", hide_title_bar=True)

    chain = ui2.ChainedAnimation(a_anim, b_anim, a_anim, b_anim)
    chain.play()


def demo_Transitions():
    v1 = ui.View()
    v1.width = v1.height = 500
    v1.background_color = "red"

    v2 = ui.View()
    v2.width = v2.height = 500
    v2.background_color = "blue"

    v1.present('sheet')

    ui2.transition(v1, v2, ui2.TRANSITION_CURL_UP, 1.5,
                   lambda success: print('success' if success else 'failed'))


def demo_ChainedTransition():

    v1 = ui.View()
    v1.width = v1.height = 500
    v1.background_color = "red"

    v2 = ui.View()
    v2.width = v2.height = 500
    v2.background_color = "blue"

    v3 = ui.View()
    v3.width = v3.height = 500
    v3.background_color = "lightgreen"

    v1.present("sheet")

    t1 = ui2.Transition(v1, v2, ui2.TRANSITION_CURL_UP, 1.5)
    t2 = ui2.Transition(v2, v3, ui2.TRANSITION_FLIP_FROM_LEFT, 1)
    t3 = ui2.Transition(v3, v1, ui2.TRANSITION_CROSS_DISSOLVE, 1)

    ui2.ChainedTransition(t1, t2, t3).play()


def demo_BlurView():
    a = ui.View()
    a.add_subview(ui.ImageView())
    a.subviews[0].image = ui.Image.named('test:Lenna')
    a.add_subview(ui2.BlurView())
    a.frame = a.subviews[0].frame = a.subviews[1].frame = (0, 0, 500, 500)
    a.present('sheet')

    toggle = ui2.Animation(a.subviews[1].toggle_brightness, 1)
    ui2.ChainedAnimation(toggle, toggle, toggle, toggle).play()


# DEMO RUNNER -----------------------------------------------------------------


if __name__ == "__main__":
    import dialogs

    prefix = "demo_"

    # Generate list of demos
    functions = [k for k in globals().keys() if k.startswith(prefix)]

    # Let user pick one
    demo = dialogs.list_dialog(
        "Choose a demo",
        sorted([fn.lstrip(prefix).replace("_", " ") for fn in functions])
    )

    # Run the demo
    if demo is not None:
        globals()[prefix + demo]()