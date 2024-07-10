import constclasses as cc


@cc.const_class
class Person:
    first_name: str
    last_name: str
    age: int

    def __repr__(self) -> str:
        return f"{self.first_name} {self.last_name} [age: {self.age}]"

@cc.const_class(with_strict_types=True)
class PersonStrictTypes:
    first_name: str
    last_name: str
    age: int

    def __repr__(self) -> str:
        return f"{self.first_name} {self.last_name} [age: {self.age}]"


if __name__ == "__main__":
    john = Person("John", "Doe", 21.5)
    print(f"{john = }")

    try:
        # invalid as 21.5 is not an instance of int
        john_strict = PersonStrictTypes("John", "Doe", 21.5)
    except TypeError as err:
        print(f"Error:\n{err}")

    john_strict = PersonStrictTypes("John", "Doe", 21)
    print(f"{john_strict = }")
