---
name: uv
description: Running Python code with uv (project root, uv run, venv)
---

# Running Python Code with uv

This project uses `uv` as the Python package manager. Use this skill when running scripts, tests, or the application.

## Project Structure

- **Project root**: Directory containing `pyproject.toml`
- **Source code**: Layout is project-specific (e.g. `service/`, or `src/` if present)
- **Config**: `pyproject.toml` and `uv.lock` at project root

## Running Python Code

1. **Work from project root**: Run commands from the directory that contains `pyproject.toml`.

2. **Preferred: use `uv run`**
   - No need to activate a venv manually.
   - Uses the project's virtual environment and dependencies.

   ```bash
   uv run service/main.py
   uv run pytest
   uv run python -c "from service.main import main; main()"
   ```

3. **Alternative: activate venv then run**
   - `source .venv/bin/activate` (or equivalent on Windows)
   - Then run Python or pytest as usual.

## Examples

```bash
# Run the main module
uv run service/main.py

# Run tests
uv run pytest

# Run a one-off script
uv run python scripts/some_script.py
```

`uv run` automatically uses the project's virtual environment and dependencies.
