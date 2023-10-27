""" Application configurations """
import os
import dotenv

ENV_DEV = ".dev.env"
ENV_OAUTH = ".oauth.env"
ENV_CCG = ".ccg.env"
ENV_JET = ".jwt.env"


class ConfigDev:
    """application configurations"""

    def __init__(self) -> None:
        dotenv.load_dotenv(ENV_DEV)
        # Common configurations
        self.dev_token = os.getenv("DEV_TOKEN")

    def __repr__(self) -> str:
        return f"ConfigDev({self.__dict__})"


class ConfigOAuth:
    """application configurations"""

    def __init__(self) -> None:
        dotenv.load_dotenv(ENV_OAUTH)
        # Common configurations
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")

        # OAuth2 configurations
        self.redirect_uri = os.getenv("REDIRECT_URI")
        self.callback_hostname = os.getenv("CALLBACK_HOSTNAME")
        self.callback_port = int(os.getenv("CALLBACK_PORT", 5000))

        self.cache_file = os.getenv("CACHE_FILE", ".oauth.tk")

    def __repr__(self) -> str:
        return f"ConfigOAuth({self.__dict__})"


class ConfigCCG:
    """application configurations"""

    def __init__(self) -> None:
        dotenv.load_dotenv(ENV_CCG)
        # Common configurations
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")

        # CCG configurations
        self.enterprise_id = os.getenv("ENTERPRISE_ID")
        self.ccg_user_id = os.getenv("CCG_USER_ID")

        self.cache_file = os.getenv("CACHE_FILE", ".ccg.tk")


def __repr__(self) -> str:
    return f"ConfigCCG({self.__dict__})"


class ConfigJWT:
    """application configurations"""

    def __init__(self) -> None:
        dotenv.load_dotenv(ENV_JET)

        # JWT configurations
        self.jwt_config_path = os.getenv("JWT_CONFIG_PATH")
        self.jwt_user_id = os.getenv("JWT_USER_ID")

        self.cache_file = os.getenv("CACHE_FILE", ".jwt.tk")

    def __repr__(self) -> str:
        return f"ConfigJWT({self.__dict__})"
