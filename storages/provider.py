import os
from importlib import import_module
from inspect import Signature
from os import environ
from typing import Any, Dict, Generator, Iterable, Tuple, Type

from storages.backends.base import Storage
from storages.exceptions import MissingEnvironmentVariableError


class StorageConstructorArgumentsExtractor:
    _DEFAULT_IGNORED_ARGUMENTS = ("self", "cls")

    @staticmethod
    def extract(
        storage_backend_class: Type[Storage],
        ignored_arguments: Tuple[str, ...] = _DEFAULT_IGNORED_ARGUMENTS,
    ) -> Generator[str, None, None]:
        signature = Signature.from_callable(storage_backend_class.__init__)
        return (
            parameter.name
            for _, parameter in signature.parameters.items()
            if parameter.kind is parameter.POSITIONAL_OR_KEYWORD
            and parameter.name not in ignored_arguments
        )


class EnvironmentVariablesCollector:
    _DEFAULT_PREFIX = "STORAGES_"

    @classmethod
    def collect(
        cls, names: Iterable[str], prefix: str = _DEFAULT_PREFIX
    ) -> Dict[str, Any]:
        values = {}
        for name in names:
            environment_variable_name = f"{prefix}{name.upper()}"
            value = os.environ.get(environment_variable_name)
            if value is None:
                raise MissingEnvironmentVariableError(
                    name=environment_variable_name
                )
            values[name] = value
        return values


class DynamicStorageLoader:
    _PATH_DELIMITER = "."

    @classmethod
    def load_class(cls, path: str) -> Type[Storage]:
        module_name, class_name = cls._get_module_and_class_name_from_path(
            path=path
        )
        module = import_module(module_name)
        return getattr(module, class_name)

    @classmethod
    def _get_module_and_class_name_from_path(
        cls, path: str
    ) -> Tuple[str, str]:
        parts = path.split(cls._PATH_DELIMITER)
        return cls._PATH_DELIMITER.join(parts[:-1]), parts[-1]


class StorageProvider:
    @classmethod
    def provide(cls, backend_path: str):
        backend_class = DynamicStorageLoader.load_class(path=backend_path)
        constructor_arguments = StorageConstructorArgumentsExtractor.extract(
            storage_backend_class=backend_class
        )
        constructor_argument_values = EnvironmentVariablesCollector.collect(
            names=constructor_arguments
        )
        return backend_class(**constructor_argument_values)  # type: ignore


default_storage = StorageProvider.provide(
    backend_path=environ["STORAGES_BACKEND"]
)
