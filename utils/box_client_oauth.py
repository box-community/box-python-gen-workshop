"""
Handles the box client object creation
orchestrates the authentication process
"""
import os
import logging
import dotenv
import uuid
from box_sdk_gen.client import BoxClient

from box_sdk_gen.oauth import OAuthConfig, BoxOAuth, GetAuthorizeUrlOptions
from box_sdk_gen.token_storage import FileWithInMemoryCacheTokenStorage

from utils.oauth_callback import callback_handle_request, open_browser

ENV_OAUTH = ".oauth.env"


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


def get_client_oauth(config: ConfigOAuth) -> BoxClient:
    """Returns a boxsdk Client object"""
    oauth = OAuthConfig(
        client_id=config.client_id,
        client_secret=config.client_secret,
        token_storage=FileWithInMemoryCacheTokenStorage(config.cache_file),
    )

    auth = BoxOAuth(oauth)
    access_token = auth.token_storage.get()

    # do we need to authorize the app?
    if not access_token:
        state = str(uuid.uuid4())
        options = GetAuthorizeUrlOptions(
            client_id=config.client_id,
            redirect_uri=config.redirect_uri,
            state=state,
        )
        auth_url = auth.get_authorize_url(options)
        logging.info("auth url: %s", auth_url)
        open_browser(auth_url)
        callback_handle_request(
            auth, config.callback_hostname, config.callback_port, state
        )

    access_token = auth.token_storage.get()
    if not access_token:
        raise Exception("Unable to get access token")

    auth.retrieve_token()

    return BoxClient(auth)
