# Python-base template

This service provides ...

## Getting started

### 1. Setup

This project uses **`uv`** for dependency management and requires **`Python >= 3.13`**.

Step 1: Create a virtual environment:

```sh
uv venv
```

Step 2: Activate the virtual environment, run:

```
source .venv/bin/activate
```

Step 3: Install dependencies

After activate the environment, install all dependencies, including development and optional groups, run the following command:

```sh
uv sync --all-groups
```

It installs all dependencies listed in `pyproject.toml` and install them.

Step 4: Install pre-commit hooks, run:

```
pre-commit install
```

**First time setup?**

See the detailed [UV Environment Setup Guide](.readme/uv-env-setup.md) for:

- Installing **`uv`**
- Installing and pinning **Python 3.13**
- Production vs development setup

### 2. Setting the service name (first-time or new project)

When cloning this repo or starting a new service from this base, run [`.scripts/set-service.sh`](.scripts/set-service.sh) to set your project name. It will:

- Prompt for a project name (alphanumeric, hyphens, underscores)
- Create or overwrite `.env` and `.env.local` from `.env.example`
- Set `SERVICE_NAME` in both files and update the `name` in `pyproject.toml` and the title in `README.md`

```bash
./.scripts/set-service.sh
```


### 4. Running the Application

To run the application:

```bash
uv run python -m service.main
```

If you have a `run.sh` script, you can use it instead:

```bash
./run.sh
```

### 4. Configuration (for local dev)

This project uses Pydantic Settings for type-safe, centralized configuration management. Configuration is loaded from the `.env` file in the project root.

### Environment params and secrets

Use `.env.example` as a reference template when editing your environment files.

### Using settings in code

For detailed information on how to use configuration settings in your code, see the [Settings in Code Guide](.readme/settings-in-code.md).
