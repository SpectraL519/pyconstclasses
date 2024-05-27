from .ccerror import ConstError, InitializationError


def _const_class_impl(cls):
    class ConstClass(cls):
        def __init__(self, *args):
            if len(args) != len(cls.__annotations__):
                raise InitializationError.invalid_number_of_arguments_error(
                    len(cls.__annotations__), len(args)
                )

            for i, (attr_name, attr_type) in enumerate(cls.__annotations__.items()):
                self.__dict__[attr_name] = attr_type(args[i])

        def __setattr__(self, attr_name: str, _) -> None:
            raise ConstError(cls.__name__, attr_name)

    ConstClass.__name__ = cls.__name__
    ConstClass.__module__ = cls.__module__

    return ConstClass


def const_class(cls=None):
    def _wrap(cls):
        return _const_class_impl(cls)

    return _wrap if cls is None else _wrap(cls)
