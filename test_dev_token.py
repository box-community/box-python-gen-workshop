"""Test configuration for developer token access"""

import logging
from utils.box_client_dev import ConfigDev, get_client_dev

logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)

conf = ConfigDev()


def main():
    client = get_client_dev(conf)

    me = client.users.get_user_me()
    print(f"\nHello, I'm {me.name} ({me.login}) [{me.id}]")


if __name__ == "__main__":
    main()
