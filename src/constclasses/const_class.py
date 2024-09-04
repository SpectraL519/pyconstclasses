from copy import deepcopy

from .ccerror import ConstError, InitializationError
from .const_class_base import (
    CC_BASE_ATTR_NAME,
    CC_INITIALIZED_ATTR_NAME,
    ConstClassBase,
)


def const_class_impl(
    cls,
    with_kwargs: bool,
    with_strict_types: bool,
    include: set[str],
    exclude: set[str],
    inherit_constructor: bool,
):
    class ConstClass(cls):
        def __init__(self, *args, **kwargs):
            cls_attrs = cls.__annotations__

            self.__dict__[CC_BASE_ATTR_NAME] = ConstClassBase(
                cls_attrs=cls_attrs.keys(),
                with_strict_types=with_strict_types,
                include=include,
                exclude=exclude,
            )
            self.__dict__[CC_INITIALIZED_ATTR_NAME] = False

            if inherit_constructor:
                super(ConstClass, self).__init__(*args, **kwargs)
                self._cc_initialized = True
                return
            else:
                super(ConstClass, self).__init__()

            if with_kwargs:
                for attr_name, attr_type in cls_attrs.items():
                    self.__dict__[attr_name] = self._cc_base.process_attribute_type(
                        attr_name, attr_type, kwargs.get(attr_name)
                    )
            else:
                if len(args) != len(cls_attrs):
                    raise InitializationError.invalid_number_of_arguments(
                        len(cls_attrs), len(args)
                    )

                for i, (attr_name, attr_type) in enumerate(cls_attrs.items()):
                    self.__dict__[attr_name] = self._cc_base.process_attribute_type(
                        attr_name, attr_type, args[i]
                    )

            self._cc_initialized = True

        def __setattr__(self, attr_name: str, attr_value) -> None:
            if self._cc_initialized and self._cc_base.is_const_attribute(attr_name):
                raise ConstError(cls.__name__, attr_name)
            self.__dict__[attr_name] = self._cc_base.process_attribute_type(
                attr_name, cls.__annotations__.get(attr_name), attr_value
            )

        def new(self, **kwargs):
            def _get_value(key: str):
                return kwargs.get(key, deepcopy(getattr(self, key)))

            if with_kwargs:
                init_params = {key: _get_value(key) for key in self.__annotations__}
                return ConstClass(**init_params)
            else:
                init_params = [_get_value(key) for key in self.__annotations__]
                return ConstClass(*init_params)

    ConstClass.__name__ = cls.__name__
    ConstClass.__module__ = cls.__module__

    return ConstClass


def const_class(
    cls=None,
    /,
    *,
    with_kwargs: bool = False,
    with_strict_types: bool = False,
    include: set[str] = None,
    exclude: set[str] = None,
    inherit_constructor=False,
):
    def _wrap(cls):
        return const_class_impl(
            cls, with_kwargs, with_strict_types, include, exclude, inherit_constructor
        )

    return _wrap if cls is None else _wrap(cls)
