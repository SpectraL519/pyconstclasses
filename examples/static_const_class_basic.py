import constclasses as cc


@cc.static_const_class
class ProjectConfiguration:
    name: str = "MyProject"
    version: str = "alpha"

    def __repr__(self):
        return f"Project: {self.name}\nVersion: {self.version}"


if __name__ == "__main__":
    print(f"Project configuration:\n{ProjectConfiguration}")

    try:
        ProjectConfiguration.version = "beta"
    except cc.ConstError as err:
        print(f"Error: {err}")
