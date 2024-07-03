class ConstClassBase:
    def __init__(self, /, *, with_strict_types: bool = False):
        self._with_strict_types = with_strict_types

    def process_attribute_type(self, attr_name, attr_type, attr_value):
        if self._with_strict_types:
            if not isinstance(attr_value, attr_type):
                raise TypeError(
                    f"Attribute value does not match the declared type:\n"
                    f"\tattribute: {attr_name}, declared type: {attr_type}, actual type: {type(attr_value)}"
                )

            return attr_value

        return attr_type(attr_value)
