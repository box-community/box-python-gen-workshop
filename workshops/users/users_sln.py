"""Box Shared links"""

import logging

from box_sdk_gen.client import BoxClient as Client
from box_sdk_gen import BoxAPIError
from box_sdk_gen.schemas import User
from box_sdk_gen.managers.transfer import TransferOwnedFolderOwnedBy
from utils.box_client_oauth import ConfigOAuth, get_client_oauth


logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)


def list_users(client: Client):
    """List users"""
    users = client.users.get_users()
    print(f"\nUsers:{users.total_count}")
    for user in users.entries:
        print(f"{user.name} ({user.login}) [{user.id}]")


def create_user(client: Client, name: str, login: str) -> User:
    """Create a user"""
    try:
        user = client.users.create_user(name, login=login)
    except BoxAPIError as err:
        if (
            err.response_info.status_code == 409
            and err.response_info.body.get("code", None) == "user_login_already_used"
        ):
            # User already exists, let's get it
            user = client.users.get_users(login).entries[0]
        else:
            raise err
    return user


def update_user(
    client: Client,
    user_id: str,
    name: str,
    login: str,
    phone: str,
    address: str,
) -> User:
    """Update a user"""
    user = client.users.update_user_by_id(
        user_id,
        name=name,
        login=login,
        phone=phone,
        address=address,
    )
    return user


def user_transfer(client: Client, source_user_id: str, destination_user_id: str):
    owned_by = TransferOwnedFolderOwnedBy(destination_user_id)
    client.transfer.transfer_owned_folder(source_user_id, owned_by)


def delete_user(client: Client, user_id: str):
    client.users.delete_user_by_id(user_id)


def main():
    """Simple script to demonstrate how to use the Box SDK"""
    conf = ConfigOAuth()
    client = get_client_oauth(conf)

    me = client.users.get_user_me()
    print(f"\nHello, I'm {me.name} ({me.login}) [{me.id}]")

    # list users
    list_users(client)

    # create a user
    new_user = create_user(client, "Test User", "YOUR_EMAIL+new@gmail.com")
    print(f"\nNew user: {new_user.name} ({new_user.login}) [{new_user.id}]")

    # update a user
    updt_user = update_user(
        client,
        new_user.id,
        "John Doe",
        "YOUR_EMAIL+new@gmail.com",
        "+15551234567",
        "123 Main St",
    )
    print(f"\nUpdated user: {updt_user.name} {updt_user.id}")
    print(f"Login: {updt_user.login}")

    print(f"Phone: {updt_user.phone}")
    print(f"Address: {updt_user.address}")

    # transfer content
    user_transfer(client, new_user.id, me.id)

    # delete user
    list_users(client)
    delete_user(client, new_user.id)
    list_users(client)


if __name__ == "__main__":
    main()
