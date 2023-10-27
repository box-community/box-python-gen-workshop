"""
Handles the box client object creation
orchestrates the authentication process
"""

import uuid
from box_sdk_gen.client import BoxClient

from box_sdk_gen.developer_token_auth import BoxDeveloperTokenAuth
from box_sdk_gen.oauth import OAuthConfig, BoxOAuth, GetAuthorizeUrlOptions
from box_sdk_gen.ccg_auth import BoxCCGAuth, CCGConfig
from box_sdk_gen.jwt_auth import BoxJWTAuth, JWTConfig

from box_sdk_gen.token_storage import FileWithInMemoryCacheTokenStorage


from utils.config import ConfigCCG, ConfigDev, ConfigJWT, ConfigOAuth
from utils.oauth_callback import callback_handle_request, open_browser


def get_client_dev(config: ConfigDev) -> BoxClient:
    """Returns a boxsdk Client object"""
    auth = BoxDeveloperTokenAuth(config.dev_token)
    return BoxClient(auth)


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
        open_browser(auth_url)
        callback_handle_request(config, state)

    access_token = auth.token_storage.get()
    if not access_token:
        raise Exception("Unable to get access token")

    auth.retrieve_token()

    return BoxClient(auth)


# def get_jwt_client(config: AppConfig, as_user_id: str = None) -> Client:
#     """Returns a boxsdk Client object"""

#     auth = JWTAuth.from_settings_file(config.jwt_config_path)

#     client = Client(auth)

#     if as_user_id:
#         as_user = client.user(as_user_id)
#         client.as_user(as_user)

#     return client


def get_ccg_enterprise_client(config: ConfigCCG) -> BoxClient:
    """Returns a boxsdk Client object"""

    ccg = CCGConfig(
        client_id=config.client_id,
        client_secret=config.client_secret,
        enterprise_id=config.enterprise_id,
        token_storage=FileWithInMemoryCacheTokenStorage(".ent." + config.cache_file),
    )
    auth = BoxCCGAuth(ccg)

    client = BoxClient(auth)

    return client


def get_ccg_user_client(config: ConfigCCG, user_id: str) -> BoxClient:
    """Returns a boxsdk Client object"""

    ccg = CCGConfig(
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_id=user_id,
        token_storage=FileWithInMemoryCacheTokenStorage(".user" + config.cache_file),
    )
    auth = BoxCCGAuth(ccg)
    # auth.as_user(user_id)

    client = BoxClient(auth)

    return client


def get_jwt_enterprise_client(config: ConfigJWT) -> BoxClient:
    """Returns a boxsdk Client object"""

    jwt = JWTConfig.from_config_file(
        config_file_path=config.jwt_config_path,
        token_storage=FileWithInMemoryCacheTokenStorage(".ent." + config.cache_file),
    )
    auth = BoxJWTAuth(jwt)

    client = BoxClient(auth)

    return client


def get_jwt_user_client(config: ConfigJWT, user_id: str) -> BoxClient:
    """Returns a boxsdk Client object"""

    jwt = JWTConfig.from_config_file(
        config_file_path=config.jwt_config_path,
        token_storage=FileWithInMemoryCacheTokenStorage(".user." + config.cache_file),
    )
    auth = BoxJWTAuth(jwt)
    auth.as_user(user_id)

    client = BoxClient(auth)

    return client
