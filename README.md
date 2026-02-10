# Python-base template

This service provides ...

## Getting started

### Running the Application

To run the application:

```bash
uv run python -m service.main
```

If you have a `run.sh` script, you can use it instead:

```bash
./run.sh
```

### Setting the service name (first-time or new project)

When cloning this repo or starting a new service from this base, run [`.scripts/set-service.sh`](.scripts/set-service.sh) to set your project name. It will:

- Prompt for a project name (alphanumeric, hyphens, underscores)
- Create or overwrite `.env` and `.env.local` from `.env.example`
- Set `SERVICE_NAME` in both files and update the `name` in `pyproject.toml` and the title in `README.md`

```bash
./.scripts/set-service.sh
```

### Env installation for local dev

This project uses **`uv`** for dependency management and requires **`Python >= 3.13`**.

**Quick start:**

```bash
# Development (includes dev dependencies)
uv sync --all-groups

# Activate the virtual environment
source .venv/bin/activate
```

**First time setup?**

See the detailed [UV Environment Setup Guide](.readme/uv-env-setup.md) for:

- Installing **`uv`**
- Installing and pinning **Python 3.13**
- Production vs development setup

### Configuration (for local dev)

This project uses Pydantic Settings for type-safe, centralized configuration management. Configuration is loaded from the `.env` file in the project root.

### Environment params and secrets

Use `.env.example` as a reference template when editing your environment files.

### Using settings in code

For detailed information on how to use configuration settings in your code, see the [Settings in Code Guide](.readme/settings-in-code.md).
