from typing import Any


class StoragesError(Exception):
    pass


class ImproperlyConfiguredError(StoragesError):
    def __init__(self, name: str):
        super().__init__(f"The '{name}' setting has improper value")


class MissingEnvironmentVariableError(StoragesError):
    def __init__(self, name: str):
        super().__init__(f"The environment variable '{name}' is not defined")
