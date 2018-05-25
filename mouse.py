
import time

from talon.audio import noise
from talon.voice import Key
from talon.track.geom import Point2d

try:
    import eye
except:
    import eye_mouse as eye

import time
from talon import ctrl, tap
from talon.voice import Context

ctx = Context("mouse")

x, y = ctrl.mouse_pos()
mouse_history = [(x, y, time.time())]
force_move = None


def on_move(typ, e):
    x0, y0 = mouse_history[-1][0:2]
    x, y = e.x, e.y
    if abs(x - x0) < 5 and abs(y - y0) < 5:
        return

    mouse_history.append((x, y, time.time()))


# if force_move:
#     e.x, e.y = force_move
#     return True


tap.unregister(tap.MMOVE, on_move)
tap.register(tap.MMOVE, on_move)


def click_pos(m):
    word = m._words[0]
    start = (word.start + min((word.end - word.start) / 2, 0.100)) / 1000.0
    diff, pos = min([(abs(start - pos[2]), pos) for pos in mouse_history])
    return pos[:2]


def delayed_click(m, button=0, times=1):
    old = eye.config.control_mouse
    eye.config.control_mouse = False
    x, y = click_pos(m)
    ctrl.mouse(x, y)
    ctrl.mouse_click(x, y, button=button, times=times, wait=16000)
    time.sleep(0.032)
    eye.config.control_mouse = old


def delayed_right_click(m):
    delayed_click(m, button=1)


def delayed_dubclick(m):
    delayed_click(m, button=0, times=2)


def delayed_tripclick(m):
    delayed_click(m, button=0, times=3)


def mouse_drag(m):
    x, y = click_pos(m)
    ctrl.mouse_click(x, y, down=True)


def mouse_release(m):
    x, y = click_pos(m)
    ctrl.mouse_click(x, y, up=True)


def mouse_scroll(amount):

    def scroll(m):
        print("amount is", amount)
        ctrl.mouse_scroll(x=amount)

    return scroll


def adv_click(button, *mods, **kwargs):

    def click(e):
        for key in mods:
            ctrl.key_press(key, down=True)
        delayed_click(e)
        for key in mods[::-1]:
            ctrl.key_press(key, up=True)

    return click


def control_mouse(m):
    ctrl.mouse(0, 0)
    eye.on_menu("Eye Tracking >> Control Mouse")


keymap = {
    "clicker": delayed_right_click,
    "click": delayed_click,
    "dubclick": delayed_dubclick,
    "tripclick": delayed_tripclick,
    "drag": mouse_drag,
    "release": mouse_release,
    "wheel down": mouse_scroll(20),
    "wheel up": mouse_scroll(-20),
    "click command": adv_click(0, "cmd"),
    "click control": adv_click(0, "ctrl"),
    "click option": adv_click(0, "alt"),
    "click shift": adv_click(0, "shift"),
    "click shift alt": adv_click(0, "alt", "shift"),
    "click double": adv_click(0, times=2),
    "click triple": adv_click(0, times=3),
    "click shift double": adv_click(0, "shift", times=2),
    "toggle cursor": Key("ctrl-alt-k"),
    # "debug overlay": lambda m: eye.on_menu("Eye Tracking >> Show Debug Overlay"),
    "(squid | control mouse)": control_mouse,
    # "camera overlay": lambda m: eye.on_menu("Eye Tracking >> Show Camera Overlay"),
    "(squid | run) calibration": lambda m: eye.on_menu("Eye Tracking >> Calibrate"),
}
ctx.keymap(keymap)
#
# keymap = {
#     "click drag": mouse_drag,
#     "click release": mouse_release,
#     "click left": adv_click(0),
#     "click right": adv_click(1),
#     "scrodge": mouse_scroll(10),
#     "scroop": mouse_scroll(-10),
#     "click control": adv_click(0, "ctrl"),
#     "chipper": adv_click(0, "ctrl"),
#     "click command": adv_click(0, "cmd"),
#     "click option": adv_click(0, "alt"),
#     "click shift": adv_click(0, "shift"),
#     "click shift alt": adv_click(0, "alt", "shift"),
#     "click double": adv_click(0, times=2),
#     "click triple": adv_click(0, times=3),
#     "click shift double": adv_click(0, "shift", times=2),
# }
#
# ctx.keymap(keymap)