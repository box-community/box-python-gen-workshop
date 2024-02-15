"""Box Files workshop"""

import datetime
import logging
import os
from typing import List
import shutil
import json

from box_sdk_gen.errors import BoxAPIError
from utils.box_client_oauth import ConfigOAuth, get_client_oauth
from box_sdk_gen.client import BoxClient as Client
from box_sdk_gen.schemas import File, Files
from box_sdk_gen.managers.files import CopyFileParent
from box_sdk_gen.managers.uploads import (
    PreflightFileUploadCheckParent,
    UploadFileAttributes,
    UploadFileAttributesParentField,
)
from box_sdk_gen.managers.zip_downloads import CreateZipDownloadItems
from box_sdk_gen.utils import ByteStream

logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)

SAMPLE_FOLDER = "248388439006"
SAMPLE_FILE = "1440473468727"


def upload_file(client: Client, file_path: str, folder_id: str) -> File:
    """Upload a file to a Box folder"""

    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)

    try:
        # pre-flight check

        pre_flight_arg = PreflightFileUploadCheckParent(id=folder_id)
        client.uploads.preflight_file_upload_check(
            file_name, file_size, pre_flight_arg
        )

        # upload new file
        upload_arg = UploadFileAttributes(
            file_name, UploadFileAttributesParentField(folder_id)
        )
        files: Files = client.uploads.upload_file(
            upload_arg, file=open(file_path, "rb")
        )

        box_file = files.entries[0]
    except BoxAPIError as err:
        if err.response_info.body.get("code", None) == "item_name_in_use":
            logging.warning("File already exists, updating contents")
            box_file_id = err.response_info.body["context_info"]["conflicts"][
                "id"
            ]
            try:
                # upload new version

                upload_arg = UploadFileAttributes(
                    file_name, UploadFileAttributesParentField(folder_id)
                )
                files: Files = client.uploads.upload_file_version(
                    box_file_id, upload_arg, file=open(file_path, "rb")
                )

                box_file = files.entries[0]
            except BoxAPIError as err2:
                logging.error("Failed to update %s: %s", box_file.name, err2)
                raise err2
        else:
            raise err

    return box_file


def download_file(client: Client, file_id: str, local_path_to_file: str):
    """Download a file from Box"""
    file_stream: ByteStream = client.downloads.download_file(file_id)

    with open(local_path_to_file, "wb") as file:
        shutil.copyfileobj(file_stream, file)


def download_zip(
    client: Client,
    local_path_to_zip: str,
    items: List[CreateZipDownloadItems],
):
    """Download a zip file from Box"""

    file_name = os.path.basename(local_path_to_zip)
    zip_download = client.zip_downloads.create_zip_download(items, file_name)

    file_stream: ByteStream = client.zip_downloads.get_zip_download_content(
        zip_download.download_url
    )

    with open(local_path_to_zip, "wb") as file:
        shutil.copyfileobj(file_stream, file)


def file_to_json(client: Client, file_id: str) -> str:
    """Get a file from Box"""
    file: File = client.files.get_file_by_id(file_id)
    file_json = json.dumps(file.to_dict(), indent=2)
    return file_json


def file_update_description(
    client: Client, file_id: str, description: str
) -> File:
    return client.files.update_file_by_id(file_id, description=description)


def folder_list_contents(client: Client, folder_id: str):
    folder = client.folders.get_folder_by_id(folder_id)
    items = client.folders.get_folder_items(folder_id)
    print(f"\nFolder [{folder.name}] content:")
    for item in items.entries:
        print(f"   {item.type.value} {item.id} {item.name}")


def main():
    conf = ConfigOAuth()
    client = get_client_oauth(conf)

    user = client.users.get_user_me()
    print(f"\nHello, I'm {user.name} ({user.login}) [{user.id}]")

    # make sure the folder exists
    sample_folder = client.folders.get_folder_by_id(SAMPLE_FOLDER)

    # New file upload
    sample_file = upload_file(
        client,
        "workshops/files/content_samples/sample_file.txt",
        sample_folder.id,
    )
    print(f"Uploaded {sample_file.name} to folder [{sample_folder.name}]")

    # Download file
    download_file(client, sample_file.id, "./sample_file_downloaded.txt")

    for local_file in os.listdir("./"):
        if local_file.endswith(".txt"):
            print(local_file)

    # Download zip
    user_root = client.folders.get_folder_by_id(SAMPLE_FOLDER)

    zip_items_arg = []

    for item in client.folders.get_folder_items(user_root.id).entries:
        item_arg = CreateZipDownloadItems(type=item.type, id=item.id)
        zip_items_arg.append(item_arg)

    print("Downloading zip")
    download_zip(client, "./sample_zip_downloaded.zip", zip_items_arg)

    for local_file in os.listdir("./"):
        if local_file.endswith(".zip"):
            print(local_file)

    # File information
    file = client.files.get_file_by_id(SAMPLE_FILE)
    print(f"{file.id} {file.name} {file.description}")

    file_json = file_to_json(client, SAMPLE_FILE)
    print(file_json)

    # Update a file
    file = file_update_description(
        client,
        SAMPLE_FILE,
        f"Updating the description at {datetime.datetime.now()}",
    )

    file = client.files.get_file_by_id(SAMPLE_FILE)
    print(f"{file.id} {file.name} {file.description}")

    # Copy a file
    try:
        file_copied = client.files.copy_file(
            SAMPLE_FILE,
            CopyFileParent(SAMPLE_FOLDER),
            name="sample_file_copy.txt",
        )
        file_copied_id = file_copied.id
    except BoxAPIError as err:
        if err.response_info.body.get("code", None) == "item_name_in_use":
            logging.warning("Duplicate File already exists")
            file_copied_id = err.response_info.body["context_info"][
                "conflicts"
            ]["id"]
        else:
            raise err
    folder_list_contents(client, SAMPLE_FOLDER)

    # Move a file
    try:
        file_moved = client.files.update_file_by_id(
            file_copied_id, parent=CopyFileParent("0")
        )
        file_moved_id = file_moved.id
    except BoxAPIError as err:
        if err.response_info.body.get("code", None) == "item_name_in_use":
            logging.warning("File already exists, we'll use it")
            file_moved_id = err.response_info.body["context_info"][
                "conflicts"
            ]["id"]
        else:
            raise err

    folder_list_contents(client, "0")

    # Delete a file
    client.files.delete_file_by_id(file_moved_id)
    folder_list_contents(client, "0")


if __name__ == "__main__":
    main()
