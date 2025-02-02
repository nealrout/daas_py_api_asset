import requests
from .module import funcation1
from daas_py_common.logging_config import logger

# Package-level variable
PACKAGE_NAME = "daas_api_asset"

# Package-level initialization
logger.debug(f"Initializing package {PACKAGE_NAME}")

# Package-level function
def initialize():
    logger.debug("Package initialized")

__all__ = ["initialize", "PACKAGE_NAME"]