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
    import time

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


# DEMO RUNNER -----------------------------------------------------------------


if __name__ == "__main__":
    import dialogs

    prefix = "demo_"

    # Generate list of demos
    functions = [k for k in globals().keys() if k.startswith(prefix)]

    # Let user pick one
    demo = dialogs.list_dialog(
        "Choose a demo",
        [fn.lstrip(prefix).replace("_", " ") for fn in functions]
    )

    # Run the demo
    if demo is not None:
        globals()[prefix + demo]()
