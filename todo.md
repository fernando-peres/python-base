# Template cleanup

What is needed to turn this base into a clean project (no “Hello, World” or example code).

## 1. Run set-service (first-time / new project)

When starting from this template, run:

```bash
./.scripts/set-service.sh
```

- Prompts for project name (alphanumeric, hyphens, underscores).
- Creates/overwrites `.env` and `.env.local` from `.env.example`.
- Sets `SERVICE_NAME` in env and `name` in `pyproject.toml`.

See [README.md – Setting the service name](README.md#setting-the-service-name-first-time-or-new-project).

## 2. Remove Hello, World and example from `service/main.py`

- **Remove** the `print("Hello, World!")` and the “TO DO: Remove Hello, World!” comment.
- **Remove** the example function `sum_two_numbers` and its “TO DO: Remove this example” comment.
- Keep bootstrap + logger init and the `if __name__ == "__main__"` block (without the print). Optionally keep a single `logger.info("…")` after init if you want a startup message.

## 3. Remove or replace the example unit test

- In **`tests/unit/test_main.py`**: the test `test_sum_two_numbers_with_positive_integers_returns_sum` and the import `from main import sum_two_numbers` are only for the example.
- **Either** delete this test (and the file if it becomes empty, or leave a minimal placeholder test), **or** replace it with a real test for your entrypoint (e.g. that the app starts or that bootstrap runs without error).
  
---

## Recommended read

- **README.md** – run app, set-service, env setup, config.
- **.readme/uv-env-setup.md** – installing `uv`, Python 3.13, dev vs prod.
- **.readme/settings-in-code.md** – using settings (Pydantic) in code.
