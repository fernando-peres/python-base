"""
Resource Names
"""

from enum import StrEnum, auto


class ResourceName(StrEnum):
    """
    StrEnum: **Constants - Resource names **
    Canonical names for internal system resources.

    """

    SETTINGS = auto()
    LOGGER = auto()
