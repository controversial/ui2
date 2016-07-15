import functools
import threading


def delay(func, seconds):
    """Call a function after a given delay."""
    threading.Timer(seconds, func).start()


def delayed_by(seconds):
    """Delay in decorator form."""
    return functools.partial(delay, seconds=seconds)
