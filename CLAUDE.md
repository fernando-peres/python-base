# Project Context

## Rules
Read and follow all files in `.context/rules/` before starting any task.

## Skills
Consult the relevant files in `.context/skills/` when the task matches their domain.

## Index

### Rules

- `.context/rules/architecture.md` — DDD layers, bounded contexts, endpoint constraints
- `.context/rules/python.md` — code style, typing, ruff, mypy, pre-commit
- `.context/rules/testing.md` — test structure, pytest standards
- `.context/rules/dto-naming.md` — DTO naming conventions (Command/Result, Request/Response)
- `.context/rules/logger.md` — logger injection pattern (always inject, never self.logger)

### Skills

Each skill is a folder under `.context/skills/<name>/` with `SKILL.md` (Context7 / Agent Skills format). Consult the relevant skill when the task matches.

- `.context/skills/usecase/SKILL.md` — how to implement a new use case
- `.context/skills/endpoint/SKILL.md` — how to implement a FastAPI endpoint
- `.context/skills/repository/SKILL.md` — repository method template
- `.context/skills/bootstrap-and-registry/SKILL.md` — registry, vocabulary, and bootstrap usage
- `.context/skills/migration/SKILL.md` — Alembic migration patterns
- `.context/skills/rabbitmq/SKILL.md` — exchange types, serialization, ack handling
- `.context/skills/uv/SKILL.md` — running code with uv
- `.context/skills/specs-consultation/SKILL.md` — consulting and maintaining specs
