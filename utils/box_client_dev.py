"""
Handles the box client object creation for a box application using a developer token
note: developer tokens are always associated with the user who created them
"""

import os
import dotenv

from box_sdk_gen.client import BoxClient
from box_sdk_gen import BoxDeveloperTokenAuth


ENV_DEV = ".dev.env"


class ConfigDev:
    """authentication configurations"""

    def __init__(self) -> None:
        dotenv.load_dotenv(ENV_DEV)
        # Common configurations
        self.dev_token = os.getenv("DEV_TOKEN")

    def __repr__(self) -> str:
        return f"ConfigDev({self.__dict__})"


def get_client_dev(config: ConfigDev) -> BoxClient:
    """Returns a box sdk Client object"""
    auth = BoxDeveloperTokenAuth(config.dev_token)
    return BoxClient(auth)
