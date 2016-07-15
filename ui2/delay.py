import threading
import uuid


class DelayManager(object):
    """A global manager for all delays."""
    def __init__(self):
        self._delays = {}

    def register(self, delay_obj):
        """Add a Delay object to the index."""
        if delay_obj.id in self._delays:
            print(self._delays)
            raise ValueError("Delay IDs must be unique!")
        else:
            self._delays[delay_obj.id] = delay_obj

    def cancel(self, id):
        """Cancel a delay by id."""
        # Allow access by a Delay object
        self._delays[id].cancel()

    def cancel_all(self):
        """Cancel all delays registered to this manager."""
        for id in self.delays:
            self.cancel(id)

    # Access the index

    def get(self, id):
        """Get a Delay object from its id."""
        return self._delays[id]

    @property
    def delays(self):
        return list(self._delays.keys())


# A global manager to be used as a default
delay_manager = DelayManager()


class Delay(object):
    def __init__(self, func, seconds, id=None, manager=delay_manager):
        self.function = func
        self.seconds = seconds
        self.id = str(uuid.uuid4()) if id is None else id
        self.manager = manager

        def func():
            self.function()
            self._deregister()

        self.timer = threading.Timer(self.seconds, func)

        self.manager.register(self)

    def start(self):
        self.timer.start()

    def cancel(self):
        """Stop the delay and remove it from its manager."""
        self.timer.cancel()
        self.manager._delays.pop(self.id)

    def _deregister(self):
        self.manager._delays.pop(self.id)
        self.manager = None


def delay(func, seconds, id=None, manager=delay_manager):
    """Call a function after a given delay."""
    delay = Delay(func, seconds, id, manager)
    delay.start()
    return delay.id


def delayed_by(seconds, *args, **kwargs):
    """Delay in decorator form."""
    return lambda function: delay(function, seconds, *args, **kwargs)
