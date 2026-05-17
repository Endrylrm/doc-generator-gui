import inspect

from dataclasses import dataclass
from typing import Any, Callable, Type


@dataclass
class Provider:
    implementation: Type | None = None
    factory: Callable | None = None
    singleton: bool = False


class DIContainer:
    def __init__(self):
        self.__providers: dict[Type, Provider] = {}
        self.__singletons: dict[Type, Any] = {}

    def register(
        self,
        interface: Type,
        implementation: Type | None = None,
        singleton: bool = False,
    ):
        implementation = implementation or interface
        self.__providers[interface] = Provider(
            implementation=implementation, singleton=singleton
        )

    def registerFactory(
        self,
        interface: Type,
        factory: Callable,
        singleton: bool = False,
    ):
        self.__providers[interface] = Provider(
            factory=factory,
            singleton=singleton,
        )

    def registerInstance(self, interface: Type, instance: Any):
        self._singletons[interface] = instance

    def resolve(self, interface: Type) -> Any:
        if interface in self.__singletons:
            return self.__singletons[interface]

        if interface not in self.__providers:
            raise ValueError(f"{interface} is not registered in the container.")

        provider = self.__providers[interface]

        if provider.factory:
            instance = provider.factory()

        else:
            instance = self.__create_instance(provider.implementation)

        if provider.singleton:
            self.__singletons[interface] = instance

        return instance

    def __create_instance(self, cls: Type) -> Any:
        signature = inspect.signature(cls.__init__).parameters.items()

        dependencies = [
            self.resolve(param.annotation)
            for name, param in signature
            if name != "self"
            if param.default is inspect.Parameter.empty
            if param.annotation is not inspect.Parameter.empty
        ]

        return cls(*dependencies)
