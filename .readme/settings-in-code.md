# Using Configuration in Code

The configuration is available through the centralized `settings` object:

```python
from service.config import settings

logging_level = settings.logging_level
```

Or via dependency injection:

```python
from service.shared.registry import inject
from service.shared.vocabulary import ResourceName

settings = inject(ResourceName.SETTINGS) 
logging_level = settings.logging_level
```

## Environment files

The application supports multiple environment-specific files for different deployment scenarios. A script copies the chosen file into `.env` (the active config); the source file is left unchanged, so you can switch between environments without losing data.

- **`.env.local`** – Local development environment
- **`.env.dev`** – Development server environment
- **`.env.stage`** – Staging environment
- **`.env.prd`** – Production environment
- **`.env`** – Active configuration file (used by the application)

To support more file names (e.g. `.env.qa`), add them to `.scripts/switch_env.py`.

**Note:** Environment-specific files (`.env.local`, `.env.dev`, `.env.stage`, `.env.prd`) are gitignored and must not be committed. Only `.env.example` is tracked.

## Selecting an environment

Use the `switch_env.py` script to switch between different environment configurations. The script copies the content of the selected environment file to `.env`, which is then used by the application. The original environment-specific files remain untouched.

```bash
# Switch to development environment
python .scripts/switch_env.py --dev
```

**Parameters:**

- `--local` – Local environment
- `--dev` – Development environment
- `--stage` – Staging environment
- `--prd` – Production environment

## Configuration Reference

#### Logging Settings
- `LOGGING_LEVEL` (default: `20` / INFO) - Root logger level
- `THIRD_PARTY_LOGGERS_LEVEL` (default: `20` / INFO) - Third-party library logger level

#### General Settings
- `ENVIRONMENT` (default: `"local"`) - Current environment (local, dev, stage, prd)


## Type Safety and Validation

All configuration values are validated using Pydantic:
- **Type checking** - Values are automatically converted to the correct types
- **Required fields** - Missing required values will cause startup to fail with clear error messages
- **Value validation** - Invalid values (e.g., port out of range) are caught at startup
- **IDE support** - Full autocomplete and type hints available

## Troubleshooting

**Configuration not loading?**
- Ensure the `.env` file exists in the project root
- Verify file permissions allow reading
- Check that you've switched to an environment using `switch_env.py`

**Missing required fields?**
- Check the error message for which field is missing
- Ensure all required fields are set in your active `.env` file
- Verify environment variable names match exactly (case-insensitive)

**Wrong values being used?**
- Remember: system environment variables override file values
- Verify the `.env` file contains the correct values for your current environment
- Use `switch_env.py` to switch to the correct environment if needed
- Check that the source environment file (e.g., `.env.dev`) exists and contains your values
