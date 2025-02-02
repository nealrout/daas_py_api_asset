import requests
from .module import funcation1


# Package-level variable
PACKAGE_NAME = "daas_api_asset"

# Package-level initialization
print(f"Initializing package {PACKAGE_NAME}")

# Package-level function
def initialize():
    print("Package initialized")

__all__ = ["initialize", "PACKAGE_NAME"]