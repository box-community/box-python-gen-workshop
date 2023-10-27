"""Test configuration for developer token access"""

import logging
from utils.config import ConfigJWT
from utils.box_client import get_jwt_enterprise_client, get_jwt_user_client

logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)

conf = ConfigJWT()


def main():
    client = get_jwt_enterprise_client(conf)
    me = client.users.get_user_me()
    print(f"\nHello, I'm {me.name} ({me.login}) [{me.id}]")

    user_client = get_jwt_user_client(conf, conf.jwt_user_id)
    me = user_client.users.get_user_me()
    print(f"\nHello, I'm {me.name} ({me.login}) [{me.id}]")


if __name__ == "__main__":
    main()
