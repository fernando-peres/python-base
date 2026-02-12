# Repository Method Template

Use this skill when implementing or modifying repository methods. All repository methods MUST follow the try-except-finally pattern for resource management and error handling.

## Core Requirements

1. **Session injection**: Inject the database session inside the method (e.g. via `inject_session(tenant_id=tenant_id)`). Do not use `Depends()` for session.
2. **Resource cleanup**: Always close the session in a `finally` block.
3. **Error handling**: Log errors with context, then re-raise as domain exceptions.
4. **Entity mapping**: Map database rows to domain entities; never return raw rows.
5. **Type casting**: Cast `session.execute()` results to `CursorResult[Any]` for type safety.

## Read Method Template

```python
from typing import Any, cast
from sqlalchemy.engine import CursorResult

async def find_all(self, tenant_id: str, limit: int = 100, offset: int = 0) -> list[User]:
    """Repository method following standard pattern."""
    session = None
    try:
        logger = inject(ResourceName.LOGGER)
        session = inject_session(tenant_id=tenant_id)

        sql = """
            SELECT id, email, name, created_at
            FROM users
            WHERE tenant_id = :tenant_id
            LIMIT :limit OFFSET :offset
        """
        result = cast(
            CursorResult[Any],
            await session.execute(
                sql,
                {"tenant_id": tenant_id, "limit": limit, "offset": offset},
            ),
        )

        return [
            User(
                id=UUID(row.id),
                email=row.email,
                name=row.name,
                created_at=row.created_at,
            )
            for row in result.fetchall()
        ]

    except Exception as e:
        logger.error(f"Error finding users for tenant {tenant_id}: {e}", exc_info=True)
        raise RepositoryError(f"Failed to find users: {str(e)}") from e
    finally:
        if session:
            await session.close()
```

## Write Method Template (INSERT/UPDATE/DELETE)

Use commit in the happy path and rollback on exception:

```python
async def save(self, user: User, tenant_id: str) -> User:
    session = None
    try:
        logger = inject(ResourceName.LOGGER)
        session = inject_session(tenant_id=tenant_id)

        sql = """
            INSERT INTO users (id, email, name, tenant_id)
            VALUES (:id, :email, :name, :tenant_id)
        """
        await session.execute(
            sql,
            {
                "id": str(user.id),
                "email": user.email,
                "name": user.name,
                "tenant_id": tenant_id,
            },
        )
        await session.commit()
        return user

    except Exception as e:
        if session:
            await session.rollback()
        logger.error(f"Error saving user {user.id}: {e}", exc_info=True)
        raise RepositoryError(f"Failed to save user: {str(e)}") from e
    finally:
        if session:
            await session.close()
```

## Checklist

**Every repository method:**

- Initialize `session = None` before the try block
- Inject logger: `inject(ResourceName.LOGGER)` (see `.context/rules/logger.md`)
- Inject session (e.g. `inject_session(tenant_id=tenant_id)`)
- Cast execute results: `cast(CursorResult[Any], ...)`
- Map results to domain entities
- Log errors with context and re-raise domain exceptions
- For writes: `await session.commit()` on success, `await session.rollback()` on exception
- Close session in `finally`: `await session.close()`

**Never:**

- Use `Depends()` for session
- Return raw database rows or ORM models
- Skip the finally block or forget to close sessions
- Forget commit/rollback for write operations
