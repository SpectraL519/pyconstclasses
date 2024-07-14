import constclasses as cc


@cc.const_class
class PersonArgs:
    first_name: str
    last_name: str

    def __repr__(self) -> str:
        return f"{self.first_name} {self.last_name}"


@cc.const_class(with_kwargs=True)
class PersonKwargs:
    first_name: str
    last_name: str

    def __repr__(self) -> str:
        return f"{self.first_name} {self.last_name}"


if __name__ == "__main__":
    john_args = PersonArgs("John", "Doe")
    print(f"{john_args = }")

    try:
        john_args = PersonArgs(first_name="John", last_name="Doe")
    except cc.InitializationError as err:
        print(f"Error: {err}")

    john_kwargs = PersonKwargs(first_name="John", last_name="Doe")
    print(f"{john_kwargs = }")
