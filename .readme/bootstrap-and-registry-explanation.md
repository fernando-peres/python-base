# Bootstrap and Registry

The project uses a **registry** pattern and **bootstrap** to provide shared resources (e.g. logger, settings) to the application and tests.

## Registry pattern

A **registry** is a single shared store of named dependencies. Components do not construct these themselves; they are registered at startup and later retrieved by name.

- **Implementation**: `service.shared.registry` — `Registry` class (singleton, thread-safe) with `register(name, item)` and `get(name)`.
- **Usage**: Use `inject(name)` to obtain a resource by name. It is shorthand for `Registry().get(name)`.

```python
from service.shared.registry import inject
from service.config.vocabulary import ResourceName

logger = inject(ResourceName.LOGGER)
settings = inject(ResourceName.SETTINGS)
```

## Resources (vocabulary)

**Vocabulary** is the set of canonical names for resources — the project’s keywords for what can be registered and injected.

- **Location**: `service.config.vocabulary` — the `ResourceName` StrEnum (e.g. `SETTINGS`, `LOGGER`).
- **Extending**: Add new resource types by adding members to `ResourceName` and registering them in bootstrap.

## Bootstrap

**Bootstrap** is the one-time setup that creates and registers the resources that support the app.

- **Function**: `initialize_service_resources()` in `service.config.bootstrap`.
- **Behavior**: Loads settings, configures logging, and registers resources (e.g. `ResourceName.SETTINGS`, `ResourceName.LOGGER`) into the registry.

The **main program** and **tests** should call `initialize_service_resources()` at startup when they need injected resources. Without it, calls to `inject(...)` will not find the registered items.

**Example (main entry point):**

```python
from service.config.bootstrap import initialize_service_resources
from service.config.vocabulary import ResourceName
from service.shared.registry import inject

if __name__ == "__main__":
    initialize_service_resources()
    logger = inject(ResourceName.LOGGER)
    logger.info("Service initialized")
```

**Tests**: If tests use `inject(ResourceName.LOGGER)` or other registered resources, run bootstrap at test startup (e.g. in `conftest.py` or a session-scoped fixture) so the registry is populated.
