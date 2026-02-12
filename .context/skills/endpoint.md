# How to Implement a FastAPI Endpoint

Consult this skill when adding or changing HTTP endpoints. Constraints are in `.context/rules/architecture.md` and `.context/rules/dto-naming.md`.

## Three-Layer DTO Separation

### 1. HTTP Layer (requests / responses)

Handle HTTP-specific validation and serialization:

```python
# application/dto/ or application/dtos/ (e.g. requests.py, responses.py)
from pydantic import BaseModel, EmailStr, Query

class CreateUserRequest(BaseModel):
    """HTTP request validation"""
    email: EmailStr
    name: str

class ListUsersRequest(BaseModel):
    """Query parameters"""
    limit: int = Query(20, ge=1, le=100)
    offset: int = Query(0, ge=0)

class UserResponse(BaseModel):
    """HTTP response serialization"""
    id: UUID
    email: str
    name: str
    created_at: datetime
```

### 2. Application Layer (commands / queries / results)

Pure business data for use case input/output; no HTTP concerns:

```python
# application/dto/ or application/dtos/ (e.g. commands_queries.py)
class CreateUserCommand(BaseModel):
    """Use case input"""
    email: str
    name: str

class GetUserQuery(BaseModel):
    user_id: UUID

class GetUserResult(BaseModel):
    """Use case output"""
    id: UUID
    email: str
    name: str
    created_at: datetime
```

### 3. Domain Layer (entities)

Business entities with invariants; never exposed via API. Used only inside application and infrastructure.

## Data Flow

1. HTTP Request (`*Request`) → map to Command or Query
2. Use case executes with Command/Query
3. Use case returns `*Result`
4. Map result to HTTP `*Response`

## Endpoint Implementation Steps

1. Receive HTTP request (payload and `request: Request`).
2. Get container: `container = request.app.state.container`.
3. Map HTTP → Command or Query.
4. Instantiate use case with dependencies from container (e.g. `CreateUserUseCase(container.user_repository())`).
5. Call `await use_case.execute(command)` (or execute with query).
6. Map domain exceptions to HTTP exceptions (e.g. 422, 404).
7. Map `*Result` to `*Response` and return.

Example:

```python
# api/v1/users/routes.py
from fastapi import APIRouter, Request, HTTPException
from application.dto.user import CreateUserRequest, CreateUserResponse
from application.dto.commands_queries import CreateUserCommand
from application.usecase.create import CreateUserUseCase

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=CreateUserResponse, status_code=201)
async def create_user(payload: CreateUserRequest, request: Request) -> CreateUserResponse:
    container = request.app.state.container
    command = CreateUserCommand(email=payload.email, name=payload.name)
    use_case = CreateUserUseCase(container.user_repository())
    try:
        user_dto = await use_case.execute(command)
    except DomainValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return CreateUserResponse(
        id=user_dto.id,
        email=user_dto.email,
        name=user_dto.name,
        created_at=user_dto.created_at,
    )
```

## Container Access

- **Correct:** Get container from `request.app.state.container`; instantiate use case with repositories from container.
- **Wrong:** Do not use `Depends()` for use cases or repositories.

## Parameter Naming

- Create/insert: `payload: CreateUserRequest`
- Auth: `credentials: LoginRequest`
- Update/patch: `updates: UpdateUserRequest`
- List/filter: `filters: ListUsersRequest`

## HTTP Methods and Status Codes

- `@router.post("", status_code=201)` — Create
- `@router.get("/{id}")` — Read single
- `@router.get("")` — Read list
- `@router.patch("/{id}")` — Partial update
- `@router.put("/{id}")` — Full replacement (rare)
- `@router.delete("/{id}", status_code=204)` — Delete

## main.py / App Setup

Ensure the app has a container on `app.state.container` (e.g. in `create_app()`: `app.state.container = container`).
