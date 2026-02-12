# Python Rules for AI Agents

## Overview

This project enforces strict coding standards via ruff (linting/formatting), mypy (type checking), and pytest (testing). All code MUST pass these checks.

## Package Management

**Use UV for dependency management** - See project docs for UV usage.
- Never suggest `pip install` or `requirements.txt`

## Formatting Rules (ruff format)

- **Line length**: 98 characters max (STRICTLY ENFORCED - E501 error)
- **Python version**: 3.13 (use modern syntax)
- **Quotes**: Double quotes only
- **Indentation**: 4 spaces (no tabs)
- **Trailing commas**: Keep them in multi-line structures

### Line Length Enforcement

**CRITICAL**: All lines MUST be ≤ 98 characters. When writing code, proactively break long lines.

**Common patterns for breaking long lines:**

```python
# ❌ BAD: Line exceeds 98 characters
logger.error(f"Event {request.id} does not exist. Please create the event first or verify the event ID is correct.")

# ✅ GOOD: Break into multiple string literals
logger.error(
    f"Event {request.id} does not exist. "
    "Please create the event first or verify the event ID is correct."
)

# ❌ BAD: Long function call
response = requests.put(url, headers=headers, files=files, timeout=30, allow_redirects=True)

# ✅ GOOD: Break function arguments across lines
response = requests.put(
    url,
    headers=headers,
    files=files,
    timeout=30,
    allow_redirects=True,
)
```

**When writing code, always:**
1. Check line length mentally before writing
2. Break long strings into multiple literals (Python automatically concatenates adjacent strings)
3. Break function calls/definitions across multiple lines
4. Shorten variable names or expressions if needed
5. Use parentheses for implicit line continuation

```python
# GOOD: Modern Python 3.13
def get_resource[T](resource_id: int) -> T | None:
    ...

def find_user(id: int | str) -> User | None:
    ...

# BAD: Old syntax
from typing import Optional, Union
def find_user(id: Union[int, str]) -> Optional[User]:
    ...
```

## Ruff Linting Rules

Enabled categories: **E, F** (PEP 8/undefined names), **B** (bugbear), **I** (isort), **UP** (pyupgrade), **SIM** (simplify), **C90** (complexity).

### Key Rules

**E, F (PEP 8/Pyflakes):**
- No undefined names or unused imports/variables
- Proper whitespace around operators
- Prefix unused variables with `_`

**B (Bugbear):**
- No mutable default arguments → use `None` as default
- No bare `except:` → catch specific exceptions
- No `assert` for validation → use proper error handling

**I (isort):** Import order: stdlib → third-party → first-party

**UP (pyupgrade):** Use modern syntax (`list[str]` not `List[str]`, f-strings, `|` unions)

**SIM (simplify):** Remove redundant conditions, unnecessary else blocks

**C90 (complexity):** Keep functions simple, break complex ones down

### Complexity Management (C901)

**CRITICAL**: Functions MUST have complexity ≤ 10. If complexity exceeds 10, refactor immediately. Extract helper methods for error handling, data transformation, and validation.

### Critical Import Rule

**DO NOT include `src` in import paths** - project root is the package root:

```python
# BAD
from src.service.interfaces.rest_v1 import health

# GOOD
from service.interfaces.rest_v1 import health
```

## Mypy Type Checking (Strict Mode)

**All functions MUST have complete type annotations.**

- All functions need parameter + return types.
- Functions without returns MUST use `-> None`.
- Generic types MUST specify parameters (e.g. `dict[str, str]` not `dict`).
- Handle None values before operations.

## Modern Python 3.13 Features

- **Type parameters**: `def get[T](id: int) -> T | None:`
- **Unions**: `int | str` not `Union[int, str]`
- **Type aliases**: `type UserID = int`
- **F-strings**: Always use f-strings for formatting

## Code Quality

- Low complexity; early returns; no mutable defaults; catch specific exceptions.

## Testing

See `.context/rules/testing.md` for test structure and pytest standards.

## Pre-commit

Code must pass `uv run pre-commit run --all-files`. Follow these to avoid common failures.

**Ruff:**
- **SIM102**: Prefer one `if` with `and` over nested `if`s. Combine conditions into a single condition.
- **C901**: Function complexity must be ≤ 10. Extract helper functions or use early `continue`/`return` to reduce branches.
- **Ruff format**: Line length 98, double quotes, trailing commas. Run `ruff format` if needed.

**Mypy:**
- **attr-defined**: Before using `.value`, `.attr`, `.id` on AST nodes, narrow the type (e.g. `isinstance(node.func, ast.Attribute)` then assign to a local or use `node.func` so mypy knows it is `ast.Attribute`).
- **arg-type**: When adding to `set[str]`, ensure the value is `str` (e.g. `ast.Constant.value` can be other types; use `isinstance(x, str)` before `set.add(x)`).

**Before committing:**

```bash
uv run pre-commit run --all-files
```

Re-run after fixes and re-stage any modified files.

## Summary

- **Ruff**: Formatting + linting (E, F, B, I, UP, SIM, C90)
- **Mypy**: Strict type checking (all functions typed)
- **Pytest**: See `.context/rules/testing.md` for testing standards

All code MUST pass these checks. Refer to `pyproject.toml` for exact configurations.
