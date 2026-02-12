# How to Implement a New Use Case

## Overview

Use cases live in `application/usecase/`. They receive a command or query DTO and return a result DTO. Dependencies (e.g. repositories) are injected via constructor, not via FastAPI `Depends()`.

## Steps

1. **Define DTOs** in `application/dto/` (or `application/dtos/`):
   - Input: a class ending with `*Command` (or query DTO for read-only use cases).
   - Output: a class ending with `*Result`.
   - See `.context/rules/architecture.md` for DTO naming and layering.

2. **Implement the use case class** in `application/usecase/`:
   - Constructor accepts the dependencies (e.g. repository, gateway).
   - Single public method, e.g. `execute(self, command: XCommand) -> XResult`.
   - No HTTP or framework concerns; pure business logic and orchestration.

3. **Wire in the API**:
   - In the endpoint, get the container from `request.app.state.container`.
   - Build the command from the HTTP request DTO (map `*Request` → `*Command`).
   - Instantiate the use case with dependencies from the container.
   - Call `execute(command)` and map the `*Result` to the HTTP `*Response`.

4. **Tests**:
   - Unit test the use case with fake repositories/gateways.
   - Integration tests can hit the API and assert on HTTP and persistence.
   - Follow `.context/rules/testing.md` for structure and naming.

## Example signature

```python
# application/usecase/create.py
class CreatePredictionUseCase:
    def __init__(self, repository: PredictionRepository) -> None:
        self._repository = repository

    def execute(self, command: CreatePredictionCommand) -> CreatePredictionResult:
        ...
```

## Reference

- DTO naming and layers: `.context/rules/architecture.md`
- Endpoint pattern and container usage: `.context/rules/architecture.md`
