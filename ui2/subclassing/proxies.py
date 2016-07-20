"""Platform-indpendent extensions to ProxyTypes."""
from ui2.subclassing.proxytypes import AbstractProxy, AbstractWrapper


class TypeProxy(AbstractProxy):
    """Delegates all operations to an instance of another class."""
    def __init__(self, obj_type, *args, **kwargs):
        if not isinstance(obj_type, type):
            raise ValueError("argument obj_type must be a class")
        self.__subject__ = obj_type(*args, **kwargs)


class TypeWrapper(TypeProxy, AbstractWrapper):
    """Consumes a class, allowing extra methods to be added."""
    pass
