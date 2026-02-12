# Logger Injection Rules

## Core Principle

**Logger must ALWAYS be injected using `inject(ResourceName.LOGGER)` when needed. NEVER store logger as a class member.**

## Rules

1. **Never use `self.logger`** - Logger should not be stored as a class attribute
2. **Inject at method level** - Use `logger = inject(ResourceName.LOGGER)` at the start of each method that needs logging
3. **Never use `logging.getLogger()`** - Always use the injected logger from the registry
4. **Import requirements** - Add these imports when using logger:
   ```python
   from service.shared.registry import inject
   from service.config.vocabulary import ResourceName
   ```

## Correct Pattern

```python
from service.shared.registry import inject
from service.config.vocabulary import ResourceName

class MyService:
    """Service class example."""

    def __init__(self) -> None:
        """Initialize the service.

        Note: No self.logger here!
        """
        self.connection = None

    async def connect(self) -> None:
        """Connect to service."""
        logger = inject(ResourceName.LOGGER)
        try:
            self.connection = await create_connection()
            logger.info("Connected successfully")
        except Exception as e:
            logger.error(f"Connection failed: {e}", exc_info=True)
            raise

    async def process(self, data: dict[str, Any]) -> None:
        """Process data."""
        logger = inject(ResourceName.LOGGER)
        logger.debug(f"Processing data: {data}")
        # ... process data ...
        logger.info("Processing completed")
```

## Incorrect Patterns

### ❌ BAD: Logger as class member

```python
class MyService:
    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)  # NEVER do this!

    async def process(self) -> None:
        self.logger.info("message")  # WRONG!
```

### ❌ BAD: Direct logging.getLogger() usage

```python
async def process(self) -> None:
    logger = logging.getLogger(__name__)  # WRONG! Use inject() instead
    logger.info("message")
```

## Why This Pattern?

1. **Centralized configuration** - Logger is configured once in bootstrap and reused everywhere
2. **Consistent behavior** - All modules use the same logger instance with same formatting
3. **Testability** - Easy to mock/replace logger in tests via registry
4. **No state in classes** - Logger is stateless, no need to store it
5. **Explicit dependencies** - Clear where logging is used

## Quick Checklist

**For every method that logs:**
- ✅ Inject logger: `logger = inject(ResourceName.LOGGER)`
- ✅ Use injected logger: `logger.info(...)`, `logger.error(...)`, etc.
- ✅ Add required imports: `inject` and `ResourceName`

**Never:**
- ❌ Store logger as class member: `self.logger = ...`
- ❌ Use `logging.getLogger()`
- ❌ Pass logger as parameter (inject it instead)
