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

    @property
    def description(self):
        ds = self._delays.values()
        return {d.id: d.description for d in ds}

    def __repr__(self):
        if self.delays:
            desc = self.description
            # Set up table columns. The columns are:
            # 1. ID
            ids = list(desc.keys())
            max_id_len = max(len(max(ids, key=len)), len("ID"))
            # 2. Delay
            delays = [d["delay"] for d in desc.values()]
            max_delay_len = max(len(str(max(delays))), len("Delay"))
            # 3. Function name
            functions = [d["function"] for d in desc.values()]
            max_function_len = max(
                len(max(functions, key=lambda x: len(x.__name__)).__name__),
                len("Function")
            )

            # Make an ASCII table
            out = "|"
            # The headers
            out += " ID ".ljust(max_id_len + 2) + "|"
            out += " Delay ".ljust(max_delay_len + 2) + "|"
            out += " Function ".ljust(max_function_len + 2) + "|"
            out += "\n"
            # The separator
            separator_len = max_id_len + max_delay_len + max_function_len + 8
            out += "|" + "-" * separator_len + "|" + "\n"
            # The body
            for id in ids:
                d = desc[id]
                out += "| {} | {} | {} |\n".format(
                    id.ljust(max_id_len),
                    str(d["delay"]).ljust(max_delay_len),
                    d["function"].__name__.ljust(max_function_len)
                )

            return out

        else:
            return ("| ID | Delay | Function |\n"
                    "|-----------------------|\n"
                    "|    |       |          |\n")

    def __str__(self):
        return self.__repr__()

# A global manager to be used as a default
delay_manager = DelayManager()


class Delay(object):
    def __init__(self, func, seconds, id=None, manager=delay_manager):
        self.function = func
        self.seconds = seconds
        self.id = id or str(uuid.uuid4())
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

    # Access data
    @property
    def description(self):
        return {
            "id": self.id,
            "delay": self.seconds,
            "function": self.function
        }

    def __repr__(self):
        return "ui2.Delay ({})".format(self.id)

    def __str__(self):
        return self.id


def delay(func, seconds, id=None, manager=delay_manager):
    """Call a function after a given delay."""
    delay = Delay(func, seconds, id, manager)
    delay.start()
    return delay.id


def delayed_by(seconds, *args, **kwargs):
    """Delay in decorator form."""
    return lambda function: delay(function, seconds, *args, **kwargs)
