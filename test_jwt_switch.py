"""Test configuration for developer token access"""

import logging
from utils.box_client_jwt import ConfigJWT
from box_sdk_gen.client import BoxClient
from box_sdk_gen import BoxJWTAuth, JWTConfig
from box_sdk_gen import FileWithInMemoryCacheTokenStorage

logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)


def main():
    config = ConfigJWT()
    jwt = JWTConfig.from_config_file(
        config_file_path=config.jwt_config_path,
        token_storage=FileWithInMemoryCacheTokenStorage(".ent" + config.cache_file),
    )

    auth = BoxJWTAuth(jwt)
    client = BoxClient(auth)
    me = client.users.get_user_me()
    print(f"\nHello, I'm {me.name} ({me.login}) [{me.id}]")

    auth = auth.with_user_subject(config.jwt_user_id)
    client = BoxClient(auth)
    me = client.users.get_user_me()
    print(f"\nHello, I'm {me.name} ({me.login}) [{me.id}]")

    auth = auth.with_user_subject("29598695136")
    client = BoxClient(auth)
    me = client.users.get_user_me()
    print(f"\nHello, I'm {me.name} ({me.login}) [{me.id}]")

    auth = auth.with_enterprise_subject(config.enterprise_id)
    client = BoxClient(auth)
    me = client.users.get_user_me()
    print(f"\nHello, I'm back to {me.name} ({me.login}) [{me.id}]")


if __name__ == "__main__":
    main()
