"""Workshop: Watermark"""

import logging

from box_sdk_gen.client import BoxClient as Client
from box_sdk_gen.fetch import APIException
from box_sdk_gen.schemas import (
    Watermark,
)

from box_sdk_gen.managers.file_watermarks import (
    UpdateFileWatermarkWatermark,
    UpdateFileWatermarkWatermarkImprintField,
)

from box_sdk_gen.managers.folder_watermarks import (
    UpdateFolderWatermarkWatermark,
    UpdateFolderWatermarkWatermarkImprintField,
)

from utils.box_client_oauth import ConfigOAuth, get_client_oauth

logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)

DEMO_FOLDER = "244798382350"
DEMO_FILE = "1418524151903"


def add_watermark_to_file(client: Client, file_id: str) -> Watermark:
    """Watermark a file"""
    update_watermark = UpdateFileWatermarkWatermark(
        UpdateFileWatermarkWatermarkImprintField.DEFAULT
    )
    return client.file_watermarks.update_file_watermark(
        file_id=file_id,
        watermark=update_watermark,
    )


def remove_watermark_from_file(client: Client, file_id: str) -> Watermark:
    """Remove watermark from file"""
    return client.file_watermarks.delete_file_watermark(file_id=file_id)


def add_watermark_to_folder(client: Client, folder_id: str) -> Watermark:
    """Watermark a folder"""
    update_watermark = UpdateFolderWatermarkWatermark(
        UpdateFolderWatermarkWatermarkImprintField.DEFAULT
    )
    return client.folder_watermarks.update_folder_watermark(
        folder_id=folder_id,
        watermark=update_watermark,
    )


def remove_watermark_from_folder(client: Client, folder_id: str) -> Watermark:
    """Remove watermark from folder"""
    return client.folder_watermarks.delete_folder_watermark(
        folder_id=folder_id
    )


def main():
    """Simple script to demonstrate how to use the Box SDK"""
    conf = ConfigOAuth()
    client = get_client_oauth(conf)

    me = client.users.get_user_me()
    print(f"\nHello, I'm {me.name} ({me.login}) [{me.id}]")

    # add watermark to file
    watermark = add_watermark_to_file(client, DEMO_FILE)
    print(
        f"\nWatermark:"
        f"\n  - created  at: {watermark.watermark.created_at}"
        f"\n  - modified at: {watermark.watermark.modified_at}"
    )

    # remove watermark from file
    remove_watermark_from_file(client, DEMO_FILE)
    print("\nWatermark removed")

    # add watermark to folder
    watermark = add_watermark_to_folder(client, DEMO_FOLDER)
    print(
        f"\nWatermark:"
        f"\n  - created  at: {watermark.watermark.created_at}"
        f"\n  - modified at: {watermark.watermark.modified_at}"
    )

    # remove watermark from folder
    remove_watermark_from_folder(client, DEMO_FOLDER)
    print("\nWatermark removed")


if __name__ == "__main__":
    main()
