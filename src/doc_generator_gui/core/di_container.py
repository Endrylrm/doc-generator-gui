import inspect

from typing import Any, Callable, Type

from .providers import Provider


class DIContainer:
    def __init__(self):
        self._providers: dict[Type, Provider] = {}
        self._singletons: dict[Type, Any] = {}

        self._reflectionCache: dict[Type, list[Any]] = {}

    def register(
        self,
        interface: Type,
        implementation: Type | None = None,
        singleton: bool = False,
    ):
        implementation = implementation or interface
        self._providers[interface] = Provider(
            implementation=implementation, singleton=singleton
        )

    def registerFactory(
        self,
        interface: Type,
        factory: Callable,
        singleton: bool = False,
    ):
        self._providers[interface] = Provider(factory=factory, singleton=singleton)

    def registerInstance(self, interface: Type, instance: Any):
        self._singletons[interface] = instance

    def resolve(self, interface: Type) -> Any:
        if interface in self._singletons:
            return self._singletons[interface]

        if interface not in self._providers:
            raise ValueError(f"{interface} is not registered in the container.")

        provider = self._providers[interface]

        instance = self._build(provider)

        if provider.singleton:
            self._singletons[interface] = instance

        return instance

    def _build(self, provider: Provider):
        if provider.factory:
            return provider.factory()

        if provider.implementation:
            return self._createInstance(provider.implementation)

    def _getReflection(self, cls: Type) -> list[Any]:
        signature = inspect.signature(cls.__init__).parameters.items()

        dependencies = [
            self.resolve(param.annotation)
            for name, param in signature
            if name != "self"
            if param.default is inspect.Parameter.empty
            if param.annotation is not inspect.Parameter.empty
        ]

        self._reflectionCache[cls] = dependencies

        return dependencies

    def _createInstance(self, cls: Type) -> Any:
        if cls in self._reflectionCache:
            return cls(*self._reflectionCache[cls])

        dependencies = self._getReflection(cls)

        return cls(*dependencies)
