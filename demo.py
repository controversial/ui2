import ui
import ui2


def _f(*args, **kwargs):
    print('Hello')


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
    v = ui.View(background_color="white")
    v.width = v.height = 500
    v.add_subview(pv)
    v.present("sheet", hide_title_bar=True)
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

    ppv = ui2.ProgressPathView(p)

    view = ui.View(background_color="white")
    view.add_subview(ppv)
    view.width = view.height = ppv.width = ppv.height = 500
    view.present("sheet", hide_title_bar=True)

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
    v = ui.View(frame=(0, 0, 500, 500), background_color="red")
    b = ui.View(frame=(100, 200, 100, 100), background_color="white")
    v.add_subview(b)

    def a():
        b.x = 300

    v.present("sheet", hide_title_bar=True)

    ui2.animate(a, 0.25, 0.25, _f)


def demo_ChainedAnimation():
    v = ui.View(frame=(0, 0, 500, 500), background_color="red")
    b = ui.View(frame=(100, 200, 100, 100), background_color="white")
    v.add_subview(b)

    def animation_a():
        b.x = 300

    def animation_b():
        b.x = 100

    a_anim = ui2.Animation(animation_a, 1, easing=ui2.ANIMATE_EASE_IN)
    b_anim = ui2.Animation(animation_b, 1, easing=ui2.ANIMATE_EASE_OUT)

    v.present("sheet", hide_title_bar=True)

    chain = ui2.ChainedAnimation(a_anim, b_anim, a_anim, b_anim, completion=_f)
    chain.play()


def demo_Transition():
    v1 = ui.View(frame=(0, 0, 500, 500), background_color="red")
    v2 = ui.View(background_color="blue")
    v1.present('sheet', hide_title_bar=True)
    ui2.transition(v1, v2, ui2.TRANSITION_CURL_UP, 1.5, _f)


def demo_ChainedTransition():
    v1 = ui.View(frame=(0, 0, 500, 500), background_color="pink")
    v1.add_subview(ui.Button(frame=(100, 100, 300, 20)))
    v1.subviews[0].title = "Hello! I'm a button"
    v1.add_subview(ui.Slider(frame=(100, 300, 100, 20)))
    v2 = ui.View(background_color="lightblue")
    v2.add_subview(ui.ImageView(frame=(100, 100, 300, 300)))
    v2.subviews[0].image = ui.Image.named('test:Peppers')
    v3 = ui.View(background_color="lightgreen")
    v3.add_subview(ui.Switch(frame=(100, 100, 20, 10)))
    v3.subviews[0].value = True

    t1 = ui2.Transition(v1, v2, ui2.TRANSITION_CURL_UP, 1.5)
    t2 = ui2.Transition(v2, v3, ui2.TRANSITION_FLIP_FROM_LEFT, 1)
    t3 = ui2.Transition(v3, v1, ui2.TRANSITION_CROSS_DISSOLVE, 1)

    v1.present("sheet", hide_title_bar=True)

    ui2.delay(ui2.ChainedTransition(t1, t2, t3).play, 1)


def demo_BlurView():
    a = ui.View(frame=(0, 0, 500, 500))
    a.add_subview(ui.ImageView(frame=(0, 0, 500, 500)))
    a.subviews[0].image = ui.Image.named('test:Peppers')
    a.add_subview(ui2.BlurView())
    a.subviews[1].frame = (100, 100, 100, 100)
    a.present('sheet', hide_title_bar=True)

    toggle = ui2.Animation(a.subviews[1].toggle_brightness, 0.5)
    def movea():
        a.subviews[1].x = 300
    def moveb():
        a.subviews[1].y = 300
    def movec():
        a.subviews[1].x = 100
    def moved():
        a.subviews[1].y = 100
    movea = ui2.Animation(movea, 1)
    moveb = ui2.Animation(moveb, 1)
    movec = ui2.Animation(movec, 1)
    moved = ui2.Animation(moved, 1)
    ui2.ChainedAnimation(movea, moveb, movec, moved, toggle,
                         movea, moveb, movec, moved).play()


def demo_Delays():
    print("* Starting *")
    print()
    print("Delays in ui2.delay_manager:")
    print(ui2.delay_manager)
    print()

    @ui2.delayed_by(2, id="Hello")
    def func():
        print("* Finished *")
        print()

    # On a different manager, this won't show up in results!
    @ui2.delayed_by(2.1, manager=ui2.DelayManager())
    def print_at_end():
        print("Delays in ui2.delay_manager:")
        print(ui2.delay_manager)

    print("* Started *")
    print()
    print("Delays in ui2.delay_manager:")
    print(ui2.delay_manager)
    print()


def demo_Status_Bar():
    ui2.statusbar.color = 0
    ui2.statusbar.background_color = "#ff8"
    print("Look at the status bar!")
    ui2.delay(ui2.statusbar.reset, 15)


def demo_Screen():
    print(ui2.screen)


def demo_CameraView():
    from ui2.view_classes.CameraView import CameraView
    a = CameraView()
    a.background_color = "#fff"
    a.start()
    a.present()
    a.will_close = lambda: a.stop()


# DEMO RUNNER -----------------------------------------------------------------


if __name__ == "__main__":
    import dialogs

    prefix = "demo_"

    # Generate list of demos
    functions = [k for k in globals().keys() if k.startswith(prefix)]

    # Let user pick one
    demo = dialogs.list_dialog(
        "Choose a demo",
        sorted([fn.replace(prefix, "").replace("_", " ") for fn in functions],
               key=lambda x: x.lower())
    )

    # Run the demo
    if demo is not None:
        globals()[prefix + demo.replace(" ", "_")]()
