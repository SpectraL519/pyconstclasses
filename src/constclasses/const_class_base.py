from .ccerror import ConfigurationError

CC_BASE_ATTR_NAME = "_cc_base"
CC_INITIALIZED_ATTR_NAME = "_cc_initialized"
MANDATORY_CONST_ATTRS = {CC_BASE_ATTR_NAME, CC_INITIALIZED_ATTR_NAME}


class ConstClassBase:
    def __init__(
        self,
        /,
        cls_attrs: set[str] = set(),
        *,
        include: set[str] = None,
        exclude: set[str] = None,
        with_strict_types: bool = False,
    ):
        intersection = cls_attrs & MANDATORY_CONST_ATTRS
        if intersection:
            raise ConfigurationError(
                f"Const class cannot have members: [{', '.join(intersection)}]"
            )

        if include is not None and exclude is not None:
            raise ConfigurationError(
                "`include` and `exclude` parameters cannot be used simultaneously"
            )

        if include is not None and not isinstance(include, set):
            include = set(include)

        if exclude is not None:
            if not isinstance(exclude, set):
                exclude = set(exclude)

            intersection = exclude & MANDATORY_CONST_ATTRS
            if intersection:
                raise ConfigurationError(
                    f"attribute(s) [{', '.join(intersection)}] cannot be excluded"
                )

        self._const_attrs = None if include is None else MANDATORY_CONST_ATTRS | include
        self._mutable_attrs = exclude
        self._with_strict_types = with_strict_types

    def is_const_attribute(self, attr_name: str):
        if self._mutable_attrs is None:
            return self._const_attrs is None or attr_name in self._const_attrs
        return attr_name not in self._mutable_attrs

    def process_attribute_type(self, attr_name, attr_type, attr_value):
        if attr_type is None and MANDATORY_CONST_ATTRS:
            return attr_value

        if self._with_strict_types:
            if not isinstance(attr_value, attr_type):
                raise TypeError(
                    f"Attribute value does not match the declared type:\n"
                    f"\tattribute: {attr_name}, declared type: {attr_type}, actual type: {type(attr_value)}"
                )

            return attr_value

        return attr_type(attr_value)
