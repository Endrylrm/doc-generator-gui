import inspect

from typing import Any, Callable, Type

from .providers import Provider


class DIContainer:
    def __init__(self):
        self.__providers: dict[Type, Provider] = {}
        self.__singletons: dict[Type, Any] = {}

        self.__reflection_cache: dict[Type, list[Any]] = {}

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
        self.__providers[interface] = Provider(factory=factory, singleton=singleton)

    def registerInstance(self, interface: Type, instance: Any):
        self.__singletons[interface] = instance

    def resolve(self, interface: Type) -> Any:
        if interface in self.__singletons:
            return self.__singletons[interface]

        if interface not in self.__providers:
            raise ValueError(f"{interface} is not registered in the container.")

        provider = self.__providers[interface]

        instance = self.__build(provider)

        if provider.singleton:
            self.__singletons[interface] = instance

        return instance

    def __build(self, provider: Provider):
        if provider.factory:
            return provider.factory()

        if provider.implementation:
            return self.__createInstance(provider.implementation)

    def __getReflection(self, cls: Type) -> list[Any]:
        signature = inspect.signature(cls.__init__).parameters.items()

        dependencies = [
            self.resolve(param.annotation)
            for name, param in signature
            if name != "self"
            if param.default is inspect.Parameter.empty
            if param.annotation is not inspect.Parameter.empty
        ]

        self.__reflection_cache[cls] = dependencies

        return dependencies

    def __createInstance(self, cls: Type) -> Any:
        if cls in self.__reflection_cache:
            return cls(*self.__reflection_cache[cls])

        dependencies = self.__getReflection(cls)

        return cls(*dependencies)
