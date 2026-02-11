# CLAUDE.md

Project-specific guidelines for Claude Code. Follow these rules when reading, writing, or modifying code in this repository.

---

## Package Management

- Use **`uv`** for all dependency management. Never suggest `pip install` or `requirements.txt`.
- Run code with `uv run <path/to/file.py>` or activate `.venv` first.
- Add deps: `uv add <package>` | dev deps: `uv add --dev <package>`

---

## Running the Project

```bash
./run.sh                              # run the service
pytest                                # run tests
pre-commit run --all-files            # run all checks (ruff + mypy)
pre-commit run --all-files --hook-stage manual  # also run pytest
```

---

## Bootstrap & Registry

Always call `initialize_service_resources()` at startup before using `inject(...)`.

```python
from service.config.bootstrap import initialize_service_resources
from service.config.vocabulary import ResourceName
from service.shared.registry import inject

initialize_service_resources()
logger = inject(ResourceName.LOGGER)
settings = inject(ResourceName.SETTINGS)
```

- `inject` → `service.shared.registry`
- `ResourceName` → `service.config.vocabulary`
- `initialize_service_resources` → `service.config.bootstrap`

To add a new resource: add a member to `ResourceName` (StrEnum) and register it in `initialize_service_resources()`.

In tests: call `initialize_service_resources()` in `conftest.py` or a session-scoped fixture before any `inject(...)` call.

---

## Logger Pattern

**Always inject logger per method. Never store as a class attribute.**

```python
from service.shared.registry import inject
from service.config.vocabulary import ResourceName

class MyService:
    async def do_something(self) -> None:
        logger = inject(ResourceName.LOGGER)  # inject at method level
        logger.info("message")
```

**Never:**
```python
self.logger = logging.getLogger(...)   # ❌ no class attribute
logger = logging.getLogger(__name__)   # ❌ no direct getLogger
```

---

## Python Coding Standards

### Formatting (Ruff)

- **Line length**: 98 characters max (strictly enforced)
- **Quotes**: double quotes only
- **Indentation**: 4 spaces
- **Python version**: 3.13 — use modern syntax

```python
# ✅ Modern syntax
def find_user(id: int | str) -> User | None: ...
type UserID = int

# ❌ Old syntax
from typing import Optional, Union
def find_user(id: Union[int, str]) -> Optional[User]: ...
```

Break long lines using parentheses or multi-line arguments:

```python
# ✅
logger.error(
    f"Event {request.id} does not exist. "
    "Please create the event first."
)
response = requests.put(
    url, headers=headers, files=files, timeout=30,
)

# ❌
logger.error(f"Event {request.id} does not exist. Please create the event first or verify the event ID is correct.")
```

### Imports

Order: **stdlib → third-party → first-party**

**Never include `src` in import paths** — `src` is the root:

```python
# ✅
from service.interfaces.rest_v1 import health

# ❌
from src.service.interfaces.rest_v1 import health
```

### Type Annotations (Mypy strict)

All functions must have complete type annotations, including `-> None`:

```python
# ✅
def process(data: list[int], count: int) -> list[int]: ...
def log_msg(msg: str) -> None: ...
def get_data() -> dict[str, str]: ...

# ❌
def process(data, count): ...          # missing types
def get_data() -> dict: ...            # unspecified generic
```

Handle `None` before operations:

```python
# ✅
def get_length(items: list[str] | None) -> int:
    return len(items) if items is not None else 0
```

### Linting Rules

Enabled: **E, F** (PEP 8), **B** (bugbear), **I** (isort), **UP** (pyupgrade), **SIM** (simplify), **C90** (complexity)

- No mutable default arguments → use `None`:
  ```python
  # ✅
  def add_item(items: list[str] | None = None) -> list[str]:
      if items is None:
          items = []
      ...
  ```
- No bare `except:` → catch specific exceptions
- No `assert` for validation

### Complexity (C901)

**Max complexity: 10.** Extract helper methods proactively when approaching 8–9:

- Single-responsibility functions
- Early returns to reduce nesting
- Extract: error handling, data transformation, validation, repeated patterns

---

## DTO Naming Conventions

Naming is determined by **where the DTO is used**, not where it is stored. DTOs live in `application/dto/`.

| Context | Input | Output |
|---|---|---|
| Use Cases (`application/usecase/`) | `*Command` | `*Result` |
| Gateways (`infrastructure/gateway/`) | `*Request` | `*Response` |
| Endpoints (`api/` or `interfaces/`) | `*Request` | `*Response` |

```python
# Use case DTOs
class CreatePredictionCommand(BaseModel): ...
class CreatePredictionResult(BaseModel): ...

# Gateway / endpoint DTOs
class GetTokenTruthSocialRequest(BaseModel): ...
class GetTokenTruthSocialResponse(BaseModel): ...
```

---

## FastAPI Architecture

**Clean Architecture**: Endpoints → Use Cases → Repositories.

Dependencies come from `request.app.state.container`. **Never use `Depends()` for use cases or repositories.**

### Data Flow

```
HTTP Request (CreateUserRequest)
  → Map to Command (CreateUserCommand)
  → Use Case executes
  → Returns Result DTO (GetUserResult)
  → Map to HTTP Response (UserResponse)
```

### DTO Locations

```
application/dtos/
├── requests.py          # HTTP input (validation, query params)
├── responses.py         # HTTP output (serialization)
├── commands_queries.py  # Use case input (*Command, *Query)
└── results.py           # Use case output (*Result)
```

### Endpoint Pattern

```python
@router.post("/users", response_model=UserResponse, status_code=201)
async def create_user(payload: CreateUserRequest, request: Request):
    container = request.app.state.container
    command = CreateUserCommand(**payload.model_dump())
    use_case = CreateUserUseCase(container.user_repository())
    result = await use_case.execute(command)
    return UserResponse(**result.model_dump())
```

### HTTP Methods & Status Codes

```python
@router.post("/users", status_code=201)        # Create
@router.get("/users/{id}")                     # Read single
@router.get("/users")                          # Read list
@router.patch("/users/{id}")                   # Partial update
@router.delete("/users/{id}", status_code=204) # Delete
```

---

## Repository Pattern

Every repository method must follow the **try-except-finally** pattern:

```python
from typing import Any, cast
from sqlalchemy.engine import CursorResult

async def find_all(self, tenant_id: str) -> list[User]:
    session = None
    try:
        logger = inject(ResourceName.LOGGER)
        session = inject_session(tenant_id=tenant_id)

        result = cast(CursorResult[Any], await session.execute(sql, params))

        return [User(...) for row in result.fetchall()]

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        raise RepositoryError(f"Failed: {str(e)}") from e
    finally:
        if session:
            await session.close()
```

For write operations add commit/rollback:

```python
await session.commit()           # after execute
await session.rollback()         # in except block, before re-raise
```

**Checklist per method:**
- `session = None` before try
- Inject logger and session inside try
- Cast `execute()` result to `CursorResult[Any]`
- Map rows to domain entities — never return raw rows
- Log errors with context (`exc_info=True`)
- Raise domain exceptions (`raise XxxError(...) from e`)
- `finally: if session: await session.close()`

**Never:**
- Use `Depends()` for session
- Return raw DB rows or ORM models
- Skip the `finally` block

---

## Testing (Pytest)

### Structure

```
tests/
├── unit/          # fast, isolated
│   ├── domain/
│   └── services/
├── integration/   # database, API
│   └── api/
└── conftest.py
```

### Naming

```python
# test_<module>.py
def test_create_user_with_valid_data_returns_user(): ...
def test_get_user_when_not_found_raises_error(): ...
```

### AAA Pattern

```python
@pytest.mark.asyncio
async def test_create_user_saves_to_database(user_repository):
    # Arrange
    user_data = {"email": "test@example.com"}
    # Act
    user = await user_repository.create(user_data)
    # Assert
    assert user.id is not None
    assert user.email == "test@example.com"
```

### Running

```bash
pytest
pytest tests/unit/test_users.py
pytest --cov=service --cov-report=term-missing
pytest -m "not slow"
```

---

## Specifications Workflow

Before implementing or modifying any feature:

1. Check `docs/specs/` for an existing spec
2. Check `docs/adr/` for related architecture decisions
3. If no spec exists, create one using `docs/specs/TEMPLATE.md`
4. Implement according to the spec
5. Add a comment referencing the spec: `# See docs/specs/feature-name-spec.md`
6. Update the spec if implementation deviates

---

## Pre-commit Summary

Hooks run on `git commit`: **Ruff** (lint + format) and **mypy** (types). Pytest is manual.

Common failure fixes:

- **SIM102**: Combine nested `if` into one with `and`
- **C901**: Complexity > 10 → extract helper methods
- **E501**: Line > 98 chars → break it
- **attr-defined** (mypy): Narrow type with `isinstance()` before accessing attributes
- **arg-type** (mypy): Guard with `isinstance(x, str)` before adding to `set[str]`

After auto-fixes: re-stage with `git add .` then commit again.
