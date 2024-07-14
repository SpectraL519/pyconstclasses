import constclasses as cc


@cc.static_const_class
class DatabaseConfiguration:
    host: str = "localhost"
    port: int = 5432
    username: str = "admin"
    password: str = "secret"

    def __repr__(self):
        return (
            f"DatabaseConfiguration:\n"
            f"Host: {self.host}\n"
            f"Port: {self.port}\n"
            f"Username: {self.username}\n"
            f"Password: {self.password}"
        )


if __name__ == "__main__":
    print(f"Database configuration:\n{DatabaseConfiguration}")

    try:
        DatabaseConfiguration.host = "remotehost"
    except cc.ConstError as err:
        print(f"Error: {err}")

    try:
        DatabaseConfiguration.port = 3306
    except cc.ConstError as err:
        print(f"Error: {err}")

    # Create a mutable instance for testing or development
    mutable_config = cc.mutable_instance(DatabaseConfiguration)
    mutable_config.host = "testhost"
    mutable_config.username = "testuser"
    mutable_config.password = "testpassword"

    print("\nMutable configuration for testing:")
    print(mutable_config)
