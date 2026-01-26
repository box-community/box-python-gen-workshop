"""
Handles the box client object creation
orchestrates the authentication process
"""

import os

import dotenv
from box_sdk_gen import (
    BoxClient,
    BoxJWTAuth,
    FileWithInMemoryCacheTokenStorage,
    JWTConfig,
)

ENV_JET = ".jwt.env"


class ConfigJWT:
    """application configurations"""

    def __init__(self) -> None:
        dotenv.load_dotenv(ENV_JET)

        # JWT configurations
        self.jwt_config_path = os.getenv("JWT_CONFIG_PATH")
        self.jwt_user_id = os.getenv("JWT_USER_ID")
        self.enterprise_id = os.getenv("ENTERPRISE_ID")

        self.cache_file = os.getenv("CACHE_FILE", ".auth.jwt")

    def __repr__(self) -> str:
        return f"ConfigJWT({self.__dict__})"


def get_jwt_enterprise_client(config: ConfigJWT) -> BoxClient:
    """Returns a box sdk Client object"""

    jwt = JWTConfig.from_config_file(
        config_file_path=config.jwt_config_path,
        token_storage=FileWithInMemoryCacheTokenStorage(f"{config.cache_file}.ent"),
    )
    auth = BoxJWTAuth(jwt)

    client = BoxClient(auth)

    return client


def get_jwt_user_client(config: ConfigJWT, user_id: str) -> BoxClient:
    """Returns a box sdk Client object"""

    jwt = JWTConfig.from_config_file(
        config_file_path=config.jwt_config_path,
        token_storage=FileWithInMemoryCacheTokenStorage(f"{config.cache_file}.user"),
    )
    auth = BoxJWTAuth(jwt)
    auth = auth.with_user_subject(user_id)

    client = BoxClient(auth)

    return client
