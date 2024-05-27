from .ccerror import ConstError, InitializationError


def static_const_class(cls):
    class StaticConstClass(cls):
        def __init__(self, *args):
            pass

        def __setattr__(self, attr_name: str, _) -> None:
            raise ConstError(cls.__name__, attr_name)

    StaticConstClass.__name__ = cls.__name__
    StaticConstClass.__module__ = cls.__module__

    return StaticConstClass()
