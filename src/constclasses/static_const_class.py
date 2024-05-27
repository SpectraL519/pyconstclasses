from .ccerror import ArgumentError, ConstError


def static_const_class(cls):
    class StaticConstClass(cls):
        def __init__(self):
            print(f"{cls.__annotations__ = }")

            static_attributes = {
                attribute: value
                for attribute, value in vars(cls).items()
                if not callable(value) and not attribute.startswith('__')
            }
            print(f"{static_attributes = }")

            super().__init__()

        def __setattr__(self, attr_name: str, _) -> None:
            raise ConstError(cls.__name__, attr_name)

    StaticConstClass.__name__ = cls.__name__
    StaticConstClass.__module__ = cls.__module__

    return StaticConstClass()


if __name__ == "__main__":
    print("Running main!")

    @static_const_class
    class StaticResource:
        x: int = 1
        s: str = "str"

    print(f"{StaticResource.x = }")
    print(f"{StaticResource.s = }")

    try:
        StaticResource.x = 3
    except ConstError as err:
        print(f"Mod x: {err}")

    try:
        StaticResource.s = "123"
    except ConstError as err:
        print(f"Mod s: {err}")

    print("Done!")
