class InitializationError(Exception):
    def __init__(self, message):
        super().__init__(message)

    @staticmethod
    def invalid_number_of_arguments_error(nexpected: int, nactual: int):
        return InitializationError(
            f"Invalid number of arguments: expected {nexpected} - got {nactual}"
        )


class ConstError(Exception):
    def __init__(self, cls_name, attribute):
        message = f"Cannot modify const attribute `{attribute}` of class `{cls_name}`"
        super().__init__(message)
