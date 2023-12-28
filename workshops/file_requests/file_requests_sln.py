"""Box Shared links"""
import logging


from box_sdk_gen.client import BoxClient as Client
from box_sdk_gen.schemas import FileRequest

from box_sdk_gen.managers.file_requests import (
    CreateFileRequestCopyFolderArg,
    CreateFileRequestCopyStatusArg,
    CreateFileRequestCopyFolderArgTypeField,
)

from utils.box_client_oauth import ConfigOAuth, get_client_oauth

# from utils.oauth_callback import open_browser

logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)

FILE_REQUEST_TEMPLATE = "7931914925"
REQUESTS_FOLDER = "241674714563"


def get_file_request(client: Client, file_request_id: str) -> FileRequest:
    return client.file_requests.get_file_request_by_id(file_request_id)


def print_file_request(file_request: FileRequest):
    print(f"\nFile Request: {file_request.id} - {file_request.title}")
    print(f"  Description: {file_request.description}")
    print(f"  Folder: {file_request.folder.id} - {file_request.folder.name}")
    print(f"  Status: {file_request.status.value}")
    print(f"  URL: {file_request.url}")


def create_file_request(
    client: Client,
    from_file_request_id: str,
    folder_id: str,
    title: str | None = None,
    description: str | None = None,
    is_email_required: bool | None = None,
    is_description_required: bool | None = None,
    expires_at: str | None = None,
) -> FileRequest:
    folder = CreateFileRequestCopyFolderArg(
        folder_id, CreateFileRequestCopyFolderArgTypeField.FOLDER
    )
    status = CreateFileRequestCopyStatusArg.ACTIVE

    file_request = client.file_requests.create_file_request_copy(
        from_file_request_id,
        folder,
        title,
        description,
        status,
        is_email_required,
        is_description_required,
        expires_at,
    )
    return file_request


def update_file_request(
    client: Client,
    file_request_id: str,
    title: str | None = None,
    description: str | None = None,
    status: CreateFileRequestCopyStatusArg | None = None,
    is_email_required: bool | None = None,
    is_description_required: bool | None = None,
    expires_at: str | None = None,
) -> FileRequest:
    file_request = client.file_requests.update_file_request_by_id(
        file_request_id,
        title,
        description,
        status,
        is_email_required,
        is_description_required,
        expires_at,
    )
    return file_request


def delete_file_request(client: Client, file_request_id: str) -> None:
    client.file_requests.delete_file_request_by_id(file_request_id)


def main():
    """Simple script to demonstrate how to use the Box SDK"""
    conf = ConfigOAuth()
    client = get_client_oauth(conf)

    user = client.users.get_user_me()
    print(f"\nHello, I'm {user.name} ({user.login}) [{user.id}]")

    file_request_template = get_file_request(client, FILE_REQUEST_TEMPLATE)
    print_file_request(file_request_template)

    # create a file request
    file_request = create_file_request(
        client,
        FILE_REQUEST_TEMPLATE,
        REQUESTS_FOLDER,
        title="File Request from SDK",
        description="This is a file request created from the Box SDK",
    )
    print_file_request(file_request)

    # update the file request
    file_request_template = update_file_request(
        client,
        FILE_REQUEST_TEMPLATE,
        title="File Request from SDK (updated)",
        description="This is a file request created from the Box SDK (updated)",
    )
    print_file_request(file_request_template)

    # delete the file requests
    delete_file_request(client, "7932431925")
    delete_file_request(client, "7932434325")
    delete_file_request(client, "7932351693")
    delete_file_request(client, "7932882833")


if __name__ == "__main__":
    main()
