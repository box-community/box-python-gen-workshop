"""Box Shared links"""
import logging
from time import sleep

from utils.box_client_oauth import ConfigOAuth, get_client_oauth
from box_sdk_gen.client import BoxClient as Client
from box_sdk_gen.schemas import (
    SignRequest,
    SignRequestCreateSigner,
    FileBaseTypeField,
    FolderBaseTypeField,
    FileBase,
    FolderMini,
)

logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)

SIGN_DOCS_FOLDER = "234102987614"

SIMPLE_PDF = "1355143830404"


def sign_doc_single(
    client: Client,
    doc_id: str,
    signer_email: str,
    sign_docs_folder: str,
    is_document_preparation_needed: bool = False,
) -> SignRequest:
    """Single doc sign by single signer"""
    # make sure file is accessible to this user
    file = client.files.get_file_by_id(file_id=doc_id)
    return client.sign_requests.create_sign_request(
        signers=[SignRequestCreateSigner(email=signer_email)],
        parent_folder=FolderMini(
            id=sign_docs_folder, type=FolderBaseTypeField.FOLDER.value
        ),
        source_files=[FileBase(id=file.id, type=FileBaseTypeField.FILE.value)],
        is_document_preparation_needed=is_document_preparation_needed,
    )


def main():
    """Simple script to demonstrate how to use the Box SDK"""
    conf = ConfigOAuth()
    client = get_client_oauth(conf)

    user = client.users.get_user_me()
    print(f"\nHello, I'm {user.name} ({user.login}) [{user.id}]")

    # Simple sign request
    simple_sign_request = sign_doc_single(
        client,
        SIMPLE_PDF,
        "barbasr@gmail.com",
        SIGN_DOCS_FOLDER,
        False,
    )
    print(f"\nSimple sign request: {simple_sign_request.id}")
    print(f"  Status: {simple_sign_request.status.value}")
    print(f"  Signers: {simple_sign_request.signers[0].email}")
    print(f"  Prepare url: {simple_sign_request.prepare_url}")


if __name__ == "__main__":
    main()
