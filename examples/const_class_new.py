import constclasses as cc


@cc.const_class(with_kwargs=True)
class PersonKwargs:
    first_name: str
    last_name: str
    age: int

    def __repr__(self) -> str:
        return f"(kwargs) {self.first_name} {self.last_name} [age: {self.age}]"


@cc.const_class(with_kwargs=False)
class PersonArgs:
    first_name: str
    last_name: str
    age: int

    def __repr__(self) -> str:
        return f"(args) {self.first_name} {self.last_name} [age: {self.age}]"


if __name__ == "__main__":
    john = PersonKwargs(first_name="John", last_name="Doe", age=21)
    print(f"{john = }")

    john_aged = john.new(age=22)
    print(f"{john_aged = }")

    john = PersonArgs("John", "Doe", 21)
    print(f"{john = }")

    john_aged = john.new(age=22)
    print(f"{john_aged = }")
