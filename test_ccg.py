"""Test configuration for developer token access"""

import logging
from utils.box_client_ccg import (
    ConfigCCG,
    get_ccg_enterprise_client,
    get_ccg_user_client,
)

logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)

conf = ConfigCCG()


def main():
    client = get_ccg_enterprise_client(conf)
    me = client.users.get_user_me()
    print(f"\nHello, I'm {me.name} ({me.login}) [{me.id}]")

    user_client = get_ccg_user_client(conf, conf.ccg_user_id)
    me = user_client.users.get_user_me()
    print(f"\nHello, I'm {me.name} ({me.login}) [{me.id}]")


if __name__ == "__main__":
    main()
