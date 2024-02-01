"""Test configuration for developer token access"""

import logging
from utils.box_client_ccg import ConfigCCG
from box_sdk_gen.client import BoxClient
from box_sdk_gen.ccg_auth import BoxCCGAuth, CCGConfig
from box_sdk_gen.token_storage import FileWithInMemoryCacheTokenStorage

logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)


def main():
    config = ConfigCCG()
    ccg = CCGConfig(
        client_id=config.client_id,
        client_secret=config.client_secret,
        enterprise_id=config.enterprise_id,
        token_storage=FileWithInMemoryCacheTokenStorage(
            ".ent" + config.cache_file
        ),
    )

    auth = BoxCCGAuth(ccg)
    client = BoxClient(auth)
    me = client.users.get_user_me()
    print(f"\nHello, I'm {me.name} ({me.login}) [{me.id}]")

    auth.as_user(config.ccg_user_id)
    me = client.users.get_user_me()
    print(f"\nHello, I'm {me.name} ({me.login}) [{me.id}]")

    auth.as_enterprise(config.enterprise_id)
    me = client.users.get_user_me()
    print(f"\nHello, I'm back to {me.name} ({me.login}) [{me.id}]")


if __name__ == "__main__":
    main()
