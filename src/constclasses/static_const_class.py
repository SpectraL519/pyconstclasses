from .ccerror import ConstError, InitializationError


def static_const_class(cls):
    class StaticConstClass(cls):
        def __init__(self, *args, **kwargs):
            self.__dict__["_initialized"] = False
            super(StaticConstClass, self).__init__(*args, **kwargs)

        def __setattr__(self, attr_name: str, value) -> None:
            if self._initialized:
                raise ConstError(cls.__name__, attr_name)
            self.__dict__[attr_name] = value

    StaticConstClass.__name__ = cls.__name__
    StaticConstClass.__module__ = cls.__module__
    StaticConstClass.__annotations__ = cls.__annotations__

    cls_vars = vars(cls)
    instance = StaticConstClass()
    for (attr_name, attr_type) in StaticConstClass.__annotations__.items():
        setattr(instance, attr_name, attr_type(cls_vars[attr_name]))
    instance._initialized = True

    return instance


def mutable_instance(static_const_cls_instance):
    static_const_cls = static_const_cls_instance.__class__
    print(static_const_cls_instance.__dict__)
    class MutableClass(static_const_cls):
        def __init__(self, *args, **kwargs):
            super(MutableClass, self).__init__(*args, **kwargs)

            for (attr_name, attr_value) in static_const_cls_instance.__dict__.items():
                self.__dict__[attr_name] = attr_value

        def __setattr__(self, attr_name, value):
            self.__dict__[attr_name] = value

    MutableClass.__name__ = f"mutable_{static_const_cls.__name__}"
    MutableClass.__module__ = static_const_cls.__module__

    return MutableClass()
