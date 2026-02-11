"""
Logger Helper Functions
"""

import logging

import colorlog

from service.config.vocabulary import ResourceName
from service.shared.registry import REGISTRY, inject
from service.shared.terminal_colors import ColorCode, coloring


# -----------------------------------------------------------------------------
# Logger Helper Class
# -----------------------------------------------------------------------------
class LoggerHelper:
    @staticmethod
    def setup_third_party_loggers() -> None:
        """
        Set up the third party loggers.
        Add the loggers of third-party libraries to the logging
        to default logging level.
        """
        settings = inject(ResourceName.SETTINGS)
        level = settings.third_party_loggers_level
        logger = inject(ResourceName.LOGGER)
        for _name, obj in logging.root.manager.loggerDict.items():
            if isinstance(obj, logging.Logger):
                logger.debug(f"Setting level for {_name} to {level}")
                obj.setLevel(level)

    # -----------------------------------------------------------------------------
    # Root Logger Configuration
    # -----------------------------------------------------------------------------
    def configure_root_logger() -> logging.Logger:
        """
        Configure the root logger.
        """
        settings = inject(ResourceName.SETTINGS)
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
        return logger
