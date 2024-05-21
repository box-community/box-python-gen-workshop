"""Test configuration for developer token access"""

import logging
from utils.box_client_ccg import ConfigCCG
from box_sdk_gen import BoxClient
from box_sdk_gen import BoxCCGAuth, CCGConfig
from box_sdk_gen import FileWithInMemoryCacheTokenStorage

logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)


def main():
    config = ConfigCCG()
    ccg = CCGConfig(
        client_id=config.client_id,
        client_secret=config.client_secret,
        enterprise_id=config.enterprise_id,
        token_storage=FileWithInMemoryCacheTokenStorage(".ent" + config.cache_file),
    )

    auth = BoxCCGAuth(ccg)
    client = BoxClient(auth)
    me = client.users.get_user_me()
    print(f"\nHello, I'm {me.name} ({me.login}) [{me.id}]")

    auth = auth.with_user_subject(config.ccg_user_id)
    client = BoxClient(auth)
    me = client.users.get_user_me()
    print(f"\nHello, I'm {me.name} ({me.login}) [{me.id}]")

    auth = auth.with_enterprise_subject(config.enterprise_id)
    client = BoxClient(auth)
    me = client.users.get_user_me()
    print(f"\nHello, I'm back to {me.name} ({me.login}) [{me.id}]")


if __name__ == "__main__":
    main()
