class ConfigurationError(Exception):
    def __init__(self, message: str):
        super().__init__(f"Invalid const class configuration: {message}")


class InitializationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

    @staticmethod
    def invalid_number_of_arguments(nexpected: int, nactual: int):
        return InitializationError(
            f"Invalid number of arguments: expected {nexpected} - got {nactual}"
        )


class ConstError(Exception):
    def __init__(self, cls_name: str, attribute: str):
        message = f"Cannot modify const attribute `{attribute}` of class `{cls_name}`"
        super().__init__(message)
