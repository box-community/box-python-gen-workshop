"""Box Shared links"""

import logging

from utils.box_client_oauth import ConfigOAuth, get_client_oauth
from box_sdk_gen.client import BoxClient as Client
from box_sdk_gen.schemas import (
    SignRequest,
    SignRequestCreateSigner,
    SignRequestPrefillTag,
    SignRequestSignerInputContentTypeField,
    FolderBaseTypeField,
    FolderMini,
    FileBase,
    FileBaseTypeField,
)

# from utils.oauth_callback import open_browser

logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)

SIGN_DOCS_FOLDER = "249194622181"

STRUCTURED_DOC = "1537410559022"

SIGNER_A = "YOUR_EMAIL+A@gmail.com"
SIGNER_A_PHONE = "+15554443322"

SIGNER_B = "YOUR_EMAIL+B@gmail.com"

APPROVER = "YOUR_EMAIL+APPROVER@gmail.com"
FINAL_COPY = "YOUR_EMAIL+FINAL_COPY@gmail.com"


def check_sign_request(sign_request: SignRequest):
    print(f"\nSimple sign request: {sign_request.id}")
    print(f"  Status: {sign_request.status.value}")
    print(f"  Signers: {len(sign_request.signers)}")
    for signer in sign_request.signers:
        print(f"    {signer.role.value}: {signer.email}")
    print(f"  Prepare url: {sign_request.prepare_url}")


def check_sign_request_by_id(client: Client, sign_request_id: str):
    """Check sign request by id"""
    sign_request = client.sign_requests.get_sign_request_by_id(sign_request_id)

    print(f"\nSimple sign request: {sign_request.id}")
    print(f"  Status: {sign_request.status.value}")

    print(f"  Signers: {len(sign_request.signers)}")
    for signer in sign_request.signers:
        print(f"    {signer.role.value}: {signer.email}")
        for input in signer.inputs:
            content_type = input.content_type
            value = None

            if content_type == SignRequestSignerInputContentTypeField.CHECKBOX:
                value = input.checkbox_value
            elif content_type == SignRequestSignerInputContentTypeField.TEXT:
                value = input.text_value
            elif content_type == SignRequestSignerInputContentTypeField.DATE:
                value = input.date_value

            print(f"      {input.type.value}: {value if value is not None else '<other>'}")

    print(f"  Prepare url: {sign_request.prepare_url}")


def create_sign_request_structured(client: Client, file_id: str, signer_email: str) -> SignRequest:
    """Create a sign request with structured data"""

    # Sign request params
    structure_file = FileBase(id=file_id, type=FileBaseTypeField.FILE)
    parent_folder = FolderMini(id=SIGN_DOCS_FOLDER, type=FolderBaseTypeField.FOLDER)
    signer = SignRequestCreateSigner(email=signer_email)

    # Create a sign request
    sign_request = client.sign_requests.create_sign_request(
        signers=[signer],
        parent_folder=parent_folder,
        source_files=[structure_file],
    )

    return sign_request


def create_sign_request_structured_with_prefill(
    client: Client, file_id: str, signer_name, signer_email: str
) -> SignRequest:
    """Create a sign request with structured data"""

    # Sign request params
    source_file = FileBase(id=file_id, type=FileBaseTypeField.FILE)
    parent_folder = FolderMini(id=SIGN_DOCS_FOLDER, type=FolderBaseTypeField.FOLDER)
    signer = SignRequestCreateSigner(email=signer_email)

    # tags
    tag_full_name = SignRequestPrefillTag(
        document_tag_id="tag_full_name",
        text_value=signer_name,
    )

    # Create a sign request
    sign_request = client.sign_requests.create_sign_request(
        signers=[signer],
        parent_folder=parent_folder,
        source_files=[source_file],
        prefill_tags=[tag_full_name],
    )

    return sign_request


def main():
    """Simple script to demonstrate how to use the Box SDK"""
    conf = ConfigOAuth()
    client = get_client_oauth(conf)

    user = client.users.get_user_me()
    print(f"\nHello, I'm {user.name} ({user.login}) [{user.id}]")

    # # Create a sign request with structured data
    # sign_request = create_sign_request_structured(client, STRUCTURED_DOC, SIGNER_A)
    # check_sign_request(sign_request)

    # # Create a sign request with name pre populate
    # sign_request_pre_pop = create_sign_request_structured_with_prefill(
    #     client, STRUCTURED_DOC, "Rui Barbosa", SIGNER_A
    # )
    # check_sign_request(sign_request_pre_pop)

    # # Latest sign request
    # LATEST_SIGN_REQUEST = "5cba6dd7-fedd-49a3-bf96-9421b1a31a83"
    # check_sign_request_by_id(client, LATEST_SIGN_REQUEST)


if __name__ == "__main__":
    main()
