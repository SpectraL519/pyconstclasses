from .ccerror import ConstError
from .const_class_base import (
    CC_BASE_ATTR_NAME,
    CC_INITIALIZED_ATTR_NAME,
    MANDATORY_CONST_ATTRS,
    ConstClassBase,
)


def static_const_class_impl(
    cls, with_strict_types: bool, include: set[str], exclude: set[str]
):
    class StaticConstClass(cls):
        def __init__(self, *args, **kwargs):
            self.__dict__[CC_BASE_ATTR_NAME] = ConstClassBase(
                cls_attrs=cls.__annotations__.keys(),
                with_strict_types=with_strict_types,
                include=include,
                exclude=exclude,
            )
            self.__dict__[CC_INITIALIZED_ATTR_NAME] = False
            super(StaticConstClass, self).__init__()

        def __setattr__(self, attr_name: str, attr_value) -> None:
            if self._cc_initialized and self._cc_base.is_const_attribute(attr_name):
                raise ConstError(cls.__name__, attr_name)
            self.__dict__[attr_name] = self._cc_base.process_attribute_type(
                attr_name, cls.__annotations__.get(attr_name), attr_value
            )

    StaticConstClass.__name__ = cls.__name__
    StaticConstClass.__module__ = cls.__module__
    StaticConstClass.__annotations__ = cls.__annotations__

    cls_vars = vars(cls)
    instance = StaticConstClass()
    for attr_name in cls.__annotations__.keys():
        setattr(instance, attr_name, cls_vars[attr_name])
    instance._cc_initialized = True

    return instance


def static_const_class(
    cls=None,
    /,
    *,
    with_strict_types: bool = False,
    include: set[str] = None,
    exclude: set[str] = None,
):
    def _wrap(cls):
        return static_const_class_impl(cls, with_strict_types, include, exclude)

    return _wrap if cls is None else _wrap(cls)


def mutable_instance(static_const_cls_instance):
    static_const_cls = static_const_cls_instance.__class__
    mutable_cls_name = f"mutable_{static_const_cls.__name__}"

    class MutableClass(static_const_cls):
        def __init__(self, *args, **kwargs):
            super(MutableClass, self).__init__(*args, **kwargs)

            for attr_name, attr_value in static_const_cls_instance.__dict__.items():
                self.__dict__[attr_name] = attr_value

        def __setattr__(self, attr_name, value):
            if attr_name in MANDATORY_CONST_ATTRS:
                raise ConstError(attr_name, mutable_cls_name)
            self.__dict__[attr_name] = value

    MutableClass.__name__ = mutable_cls_name
    MutableClass.__module__ = static_const_cls.__module__

    return MutableClass()
