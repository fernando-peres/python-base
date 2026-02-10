"""
Registry module for global storage of dependencies.
"""

from threading import Lock
from typing import Any, Self, cast


class Registry:
    """
    A simple implementation of the Registry pattern.
    This class maintains a central repository of objects or services.
    """

    _registry: dict[str, Any] = {}
    _instance: Self | None = None
    _lock: Lock = Lock()
    _initialized = False

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._initialized = True
        return cast(Self, cls._instance)

    @classmethod
    def is_initialized(cls) -> bool:
        """
        Check if the registry is initialized.

        Returns:
            bool: True if the registry is initialized, False otherwise.
        """
        return cls._initialized

    @classmethod
    def register(cls, name: str, item: Any) -> None:
        """
        Register an item in the registry.

        Args:
            name: The name under which to register the item
            item: The item to register
        """
        with cls._lock:
            if name not in cls._registry:
                cls._registry[name] = item

    @classmethod
    def unregister(cls, name: str) -> None:
        """
        Remove an item from the registry.

        Args:
            name: The name of the item to remove
        """
        with cls._lock:
            if name in cls._registry:
                del cls._registry[name]

    @classmethod
    def get(cls, name: str) -> Any:
        """
        Retrieve an item from the registry.

        Args:
            name: The name of the item to retrieve

        Returns:
            The registered item, or None if the item is not found in the registry
        """
        # return cls._registry.get(name)
        if cls._instance is None:
            cls._instance = cast(Self, super().__new__(cls))
        return cls._registry.get(name)

    @classmethod
    def count(cls) -> int:
        """
        Return the number of items in the registry.
        """

        if cls._registry:
            return len(cls._registry)
        return 0

    @classmethod
    def reset(cls) -> None:
        """
        Reset the registry by removing all registered items.
        """
        with cls._lock:
            cls._registry: dict[str, Any] = {}

    @classmethod
    def list_resources(cls) -> list[str]:
        """
        Return a list of registered resources.

        Returns:
            List of names of all registered resources.
        """
        with cls._lock:
            return list(cls._registry.keys())


def inject(name: str) -> Any:
    """
    Register an item in the registry.

    Args:
        name: The name under which to register the item
        item: The item to register
    """
    dependecy = Registry().get(name)
    return dependecy


REGISTRY = Registry()
