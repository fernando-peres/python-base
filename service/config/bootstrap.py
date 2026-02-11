"""
FastAPI application configuration & initialization.
- setup logging
- setup third party loggers
- initialize resources
"""

from service.config.settings import ServiceSettings
from service.config.vocabulary import ResourceName
from service.shared.logger import LoggerHelper
from service.shared.registry import REGISTRY, inject


# -----------------------------------------------------------------------------
# Initialize Service Resources
# -----------------------------------------------------------------------------
def initialize_service_resources() -> None:
    """
    Register the resources for the application/service.
    """
    try:
        settings = ServiceSettings()
        REGISTRY.register(ResourceName.SETTINGS, settings)
        logger = LoggerHelper.configure_root_logger()
        logger.debug("Initializing service resources...")
        LoggerHelper.setup_third_party_loggers()
    except Exception as e:
        logger = inject(ResourceName.LOGGER)
        logger.error(f"Error initializing service resources: {e}")
        raise e
