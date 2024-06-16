class InitializationError(Exception):
    def __init__(self, message):
        super().__init__(message)

    @staticmethod
    def invalid_number_of_arguments(nexpected: int, nactual: int):
        return InitializationError(
            f"Invalid number of arguments: expected {nexpected} - got {nactual}"
        )

    @staticmethod
    def static_class_initialization(cls_name: str):
        return InitializationError(f"Cannot create an instance of a static class `{cls_name}`")


class ConstError(Exception):
    def __init__(self, cls_name: str, attribute: str):
        message = f"Cannot modify const attribute `{attribute}` of class `{cls_name}`"
        super().__init__(message)
