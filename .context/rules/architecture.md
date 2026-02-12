# Architecture Rules (DDD and Layering)

## Core Principles

**Clean Architecture**: Strict separation of concerns across HTTP, Application, and Domain layers.

**Dependency Flow**: Endpoints → Use Cases → Repositories. Dependencies injected via container, never via `Depends()`.

**DTO Isolation**: All data transfer objects live in `application/dto/` (or `application/dtos/`). Domain entities are never exposed to the HTTP layer.

## Layers

### 1. HTTP Layer (API / interfaces)

- Handles HTTP-specific validation and serialization.
- Request/response DTOs use `*Request` and `*Response`. See `.context/rules/dto-naming.md` for full conventions.
- Endpoints map HTTP payloads to commands/queries, call use cases, then map results to HTTP responses.

### 2. Application Layer (use cases, DTOs)

- Use cases in `application/usecase/` receive `*Command` or query DTOs and return `*Result` DTOs.
- No HTTP concerns; pure business data in and out.
- DTOs for use cases: input `*Command`, output `*Result`.

### 3. Domain Layer (entities)

- Business entities with rules and invariants.
- Never exposed via API; only used inside application and infrastructure.

### 4. Infrastructure (gateways, persistence)

- Gateways in `infrastructure/gateway/` use DTOs with `*Request` and `*Response` for external calls.
- Repositories and other infrastructure are injected via a container, not via FastAPI `Depends()`.

## Data Flow

1. HTTP Request (`*Request`) → map to Command/Query.
2. Use case executes with Command/Query.
3. Use case returns `*Result`.
4. Map Result to HTTP `*Response`.

## DTO Naming

Full conventions: `.context/rules/dto-naming.md`. Quick reference: use cases → `*Command` / `*Result`; gateways and endpoints → `*Request` / `*Response`. Naming is determined by where the DTO is used, not where it is stored.

## Endpoint Pattern

- Get container from `request.app.state.container`.
- Instantiate use case with repositories from container.
- Do not use `Depends()` for use cases or repositories.
- Map domain exceptions to HTTP status codes in the endpoint.

## DO / DON'T

**DO:**
- Keep all DTOs in `application/dto/` or `application/dtos/` (see dto-naming.md)
- Map HTTP requests → commands/queries before use case execution
- Map use case DTOs → HTTP responses after execution
- Instantiate use cases in endpoints with repositories from container
- Use semantic parameter names (`payload`, `credentials`, `filters`, `updates`)
- Always specify `response_model` and status codes
- Handle domain exceptions → map to HTTP errors in endpoints

**DON'T:**
- Use `Depends()` for use cases or repositories
- Mix HTTP concerns (validation, query params) with commands/queries
- Return domain entities directly from endpoints
- Put business logic in route handlers
- Import infrastructure (database, repositories) in route files
- Pass repositories through endpoint parameters

**Anti-pattern (wrong):**
```python
@router.post("/users")
async def create_user(
    email: str,  # Should be in Request model
    name: str,
    repo: UserRepository = Depends(get_repo)  # Don't inject repos
):
    user = User(email=email, name=name)  # Business logic in endpoint
    saved = await repo.save(user)
    return saved  # Returning domain entity directly
```

**Correct pattern:**
```python
@router.post("/users", response_model=UserResponse, status_code=201)
async def create_user(payload: CreateUserRequest, request: Request):
    container = request.app.state.container
    command = CreateUserCommand(**payload.model_dump())
    use_case = CreateUserUseCase(container.user_repository())
    user_dto = await use_case.execute(command)
    return UserResponse(**user_dto.model_dump())
```
