from .ccerror import ConstError, InitializationError
from .const_class_base import CC_BASE_ATTR_NAME, ConstClassBase


def const_class_impl(cls, with_strict_types: bool, include: set[str], exclude: set[str]):
    class ConstClass(cls):
        def __init__(self, *args, **kwargs):
            super(ConstClass, self).__init__()

            self.__dict__[CC_BASE_ATTR_NAME] = ConstClassBase(
                with_strict_types=with_strict_types, include=include, exclude=exclude
            )

            if len(args) != len(cls.__annotations__):
                raise InitializationError.invalid_number_of_arguments(
                    len(cls.__annotations__), len(args)
                )

            for i, (attr_name, attr_type) in enumerate(cls.__annotations__.items()):
                self.__dict__[attr_name] = self._cc_base.process_attribute_type(
                    attr_name, attr_type, args[i]
                )

        def __setattr__(self, attr_name: str, attr_value) -> None:
            if self._cc_base.is_const_field(attr_name):
                raise ConstError(cls.__name__, attr_name)
            self.__dict__[attr_name] = attr_value

    ConstClass.__name__ = cls.__name__
    ConstClass.__module__ = cls.__module__

    return ConstClass


def const_class(
    cls=None,
    /,
    *,
    with_strict_types: bool = False,
    include: set[str] = None,
    exclude: set[str] = None,
):
    def _wrap(cls):
        return const_class_impl(cls, with_strict_types, include, exclude)

    return _wrap if cls is None else _wrap(cls)
