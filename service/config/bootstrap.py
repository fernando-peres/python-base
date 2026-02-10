"""
FastAPI application configuration & initialization.
- setup logging
- setup third party loggers
- initialize resources
"""

import logging

import colorlog

from service.config.settings import ServiceSettings
from service.config.vocabulary import ResourceName
from service.shared.terminal_colors import ColorCode, coloring
from service.shared.registry import REGISTRY

def setup_third_party_loggers(level: int = logging.INFO) -> None:
    """
    Set up the third party loggers.
    Add the loggers of third-party libraries to the logging
    to default logging level.
    """
    logging.getLogger("concurrent.futures").setLevel(level)
    logging.getLogger("concurrent").setLevel(level)
    logging.getLogger("asyncio").setLevel(level)
    # logging.getLogger("uvicorn").setLevel(level)
    # logging.getLogger("uvicorn.error").setLevel(level)
    # logging.getLogger("uvicorn.access").setLevel(level)
    # logging.getLogger("fastapi").setLevel(level)
    # logging.getLogger("gunicorn").setLevel(level)
    # logging.getLogger("gunicorn.access").setLevel(level)
    # logging.getLogger("gunicorn.error").setLevel(level)
    logging.getLogger("dotenv.main").setLevel(level)
    logging.getLogger("dotenv").setLevel(level)


def configure_root_logger(level: int, settings: ServiceSettings) -> None:
    """
    Configure the root logger.
    """
    level = settings.logging_level
    service_name = settings.service_name

    # Configure root logger so all modules inherit this configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s%(levelname)-9s%(reset)s %(message)s",
            log_colors={
                "DEBUG": "blue",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
    )
    root_logger.addHandler(handler)

    logger = logging.getLogger(service_name)
    logger.info(
        coloring(
            text=f"Registering resources... [{service_name}]",
            code=ColorCode.DARK_CYAN_TXT,
        )
    )
    REGISTRY.register(ResourceName.LOGGER, logger)

def configure_third_party_loggers(level: int, settings: ServiceSettings) -> None:
    """ Configure the third party loggers. """
    third_party_loggers_level = settings.third_party_loggers_level
    setup_third_party_loggers(third_party_loggers_level)

def initialize_service_resources() -> None:
    """
    Register the resources for the application/service.
    """
    settings = ServiceSettings()
    REGISTRY.register(ResourceName.SETTINGS, settings)
    configure_third_party_loggers(settings.third_party_loggers_level, settings)
    configure_root_logger(settings.logging_level, settings)
    
