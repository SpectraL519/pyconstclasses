import constclasses as cc


@cc.const_class(exclude=["age"])
class Person:
    first_name: str
    last_name: str
    age: int

    def __repr__(self) -> str:
        return f"{self.first_name} {self.last_name} [age: {self.age}]"


if __name__ == "__main__":
    john = Person("John", "Doe", 21)
    print(f"{john = }")

    try:
        john.first_name = "Bob"
    except cc.ConstError as err:
        print(f"Error: {err}")

    try:
        john.last_name = "Smith"
    except cc.ConstError as err:
        print(f"Error: {err}")

    # valid modification as the `age` parameter is in the exclude set
    john.age = 22
    print(f"{john = }")
