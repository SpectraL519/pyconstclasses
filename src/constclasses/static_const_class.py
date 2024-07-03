from .ccerror import ConstError
from .const_class_base import (
    CC_BASE_ATTR_NAME,
    CC_INITIALIZED_ATTR_NAME,
    ConstClassBase,
)


def static_const_class(cls, /, *, with_strict_types: bool = False):
    class StaticConstClass(cls):
        def __init__(self, *args, **kwargs):
            super(StaticConstClass, self).__init__(*args, **kwargs)
            self.__dict__[CC_BASE_ATTR_NAME] = ConstClassBase(
                with_strict_types=with_strict_types
            )
            self.__dict__[CC_INITIALIZED_ATTR_NAME] = False

        def __setattr__(self, attr_name: str, value) -> None:
            if self._cc_initialized:
                raise ConstError(cls.__name__, attr_name)
            self.__dict__[attr_name] = value

    StaticConstClass.__name__ = cls.__name__
    StaticConstClass.__module__ = cls.__module__
    StaticConstClass.__annotations__ = cls.__annotations__

    cls_vars = vars(cls)
    instance = StaticConstClass()
    for attr_name, attr_type in StaticConstClass.__annotations__.items():
        setattr(
            instance,
            attr_name,
            instance._cc_base.process_attribute_type(
                attr_name, attr_type, cls_vars[attr_name]
            ),
        )
    instance._cc_initialized = True

    return instance


def mutable_instance(static_const_cls_instance):
    static_const_cls = static_const_cls_instance.__class__
    print(static_const_cls_instance.__dict__)

    class MutableClass(static_const_cls):
        def __init__(self, *args, **kwargs):
            super(MutableClass, self).__init__(*args, **kwargs)

            for attr_name, attr_value in static_const_cls_instance.__dict__.items():
                self.__dict__[attr_name] = attr_value

        def __setattr__(self, attr_name, value):
            self.__dict__[attr_name] = value

    MutableClass.__name__ = f"mutable_{static_const_cls.__name__}"
    MutableClass.__module__ = static_const_cls.__module__

    return MutableClass()
