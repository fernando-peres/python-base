# Alembic Migration Patterns

## Overview

This project uses Alembic for database migrations. Follow these patterns for consistency and safety.

## Checklist

- **One logical change per migration** when possible (e.g. one table, one index).
- **Naming**: Use descriptive revision IDs and message strings (e.g. `add_users_table`, `add_index_on_email`).
- **Reversibility**: Implement `downgrade()` so migrations can be rolled back when needed.
- **No business logic**: Migrations should only change schema and reference data; avoid complex application logic.
- **Ordering**: Run migrations in order; do not edit existing migrations that have been applied in shared environments.
- **Testing**: Run migrations up and down in a test database before merging.

## Common operations

- **Add table**: `op.create_table(...)` in `upgrade`, `op.drop_table(...)` in `downgrade`.
- **Add column**: `op.add_column(...)` / `op.drop_column(...)`.
- **Add index**: `op.create_index(...)` / `op.drop_index(...)`.
- **Add constraint**: `op.create_foreign_key(...)` / `op.drop_constraint(...)`.

## Running migrations

- Generate: `alembic revision -m "description"`.
- Apply: `alembic upgrade head`.
- Rollback one revision: `alembic downgrade -1`.

Adjust commands to your project’s Alembic config (e.g. env, script location).
