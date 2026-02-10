# Using Configuration in Code

The configuration is available through the centralized `settings` object:

```python
from service.config import settings

# Access nested settings
api_key = settings.openrouter.api_key
rabbitmq_url = settings.rabbitmq.get_connection_url()
log_level = settings.logging.logging_level
```

Or via dependency injection:

```python
from service.shared.registry import inject
from service.shared.vocabulary import ResourceName

settings = inject(ResourceName.CONFIG)
rabbitmq_config = settings.rabbitmq
```

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
