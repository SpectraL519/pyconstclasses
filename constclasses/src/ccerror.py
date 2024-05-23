class ArgumentError(Exception):
    def __init__(self, nexpected, nactual):
        message = f"Invalid number of arguments: expected {nexpected} - got {nactual}"
        super().__init__(message)


class ConstError(Exception):
    def __init__(self, cls_name, attribute):
        message = f"Cannot modify const attribute `{attribute}` of class `{cls_name}`"
        super().__init__(message)
