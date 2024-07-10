import constclasses as cc


@cc.const_class(inherit_constructor=True)
class Person:
    first_name: str
    last_name: str

    def __init__(self, full_name: str):
        self.first_name, self.last_name = full_name.split(' ')

    def __repr__(self) -> str:
        return f"{self.first_name} {self.last_name}"


if __name__ == "__main__":
    john = Person("John Doe")
    print(f"{john = }")

    try:
        john.first_name = "Bob"
    except cc.ConstError as err:
        print(f"Error: {err}")

    try:
        john.last_name = "Smith"
    except cc.ConstError as err:
        print(f"Error: {err}")
