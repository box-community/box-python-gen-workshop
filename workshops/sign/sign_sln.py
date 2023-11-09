"""Box Shared links"""
import logging

from utils.box_client_oauth import ConfigOAuth, get_client_oauth
from box_sdk_gen.client import BoxClient as Client
from box_sdk_gen.schemas import (
    SignRequest,
    SignRequestCreateSigner,
    SignRequestCreateSignerRoleField,
    FileBaseTypeField,
    FolderBaseTypeField,
    FileBase,
    FolderMini,
)

from utils.oauth_callback import open_browser

logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)

SIGN_DOCS_FOLDER = "234102987614"

SIMPLE_PDF = "1355143830404"
SIMPLE_DOC = "1358077513913"
CONTRACT = "1358047520478"


def check_sign_request(sign_request: SignRequest):
    print(f"\nSimple sign request: {sign_request.id}")
    print(f"  Status: {sign_request.status.value}")
    print(f"  Signers: {sign_request.signers[0].email}")
    print(f"  Prepare url: {sign_request.prepare_url}")

    if sign_request.prepare_url is not None:
        open_browser(sign_request.prepare_url)


def sign_doc_single(
    client: Client, signer_email: str, prep_needed: bool = False
) -> SignRequest:
    """Single doc sign by single signer"""
    # make sure file is accessible to this user
    file = client.files.get_file_by_id(file_id=SIMPLE_PDF)

    signer = SignRequestCreateSigner(signer_email)
    parent_folder = FolderMini(
        id=SIGN_DOCS_FOLDER, type=FolderBaseTypeField.FOLDER.value
    )
    source_file = FileBase(id=file.id, type=FileBaseTypeField.FILE.value)

    # sign document
    sign_request = client.sign_requests.create_sign_request(
        signers=[signer],
        parent_folder=parent_folder,
        source_files=[source_file],
        is_document_preparation_needed=prep_needed,
    )

    return sign_request


def sign_contract(
    client: Client,
    institution_email: str,
    student_email: str,
) -> SignRequest:
    """Sign contract"""
    # make sure file is accessible to this user
    file = client.files.get_file_by_id(file_id=CONTRACT)

    # signers
    institution = SignRequestCreateSigner(
        email=institution_email,
        role=SignRequestCreateSignerRoleField.SIGNER,
        order=1,
    )

    student = SignRequestCreateSigner(
        email=student_email,
        role=SignRequestCreateSignerRoleField.SIGNER,
        order=2,
    )

    # create sign request
    sign_request = client.sign_requests.create_sign_request(
        signers=[institution, student],
        parent_folder=FolderMini(
            id=SIGN_DOCS_FOLDER, type=FolderBaseTypeField.FOLDER.value
        ),
        source_files=[FileBase(id=file.id, type=FileBaseTypeField.FILE.value)],
        is_document_preparation_needed=True,
    )

    return sign_request


def main():
    """Simple script to demonstrate how to use the Box SDK"""
    conf = ConfigOAuth()
    client = get_client_oauth(conf)

    # user = client.users.get_user_me()
    # print(f"\nHello, I'm {user.name} ({user.login}) [{user.id}]")

    # Simple sign a pdf request
    sign_pdf = sign_doc_single(client, "barbasr@gmail.com")
    check_sign_request(sign_pdf)

    # Simple sign a pdf request with preparation
    sign_pdf_prep = sign_doc_single(client, "barbasr@gmail.com", True)
    check_sign_request(sign_pdf_prep)
    if sign_pdf_prep.prepare_url is not None:
        open_browser(sign_pdf_prep.prepare_url)

    # Multiple signers
    sign_contract_multi = sign_contract(
        client,
        institution_email="barbasr+inst@gmail.com",
        student_email="barbasr+std@gmail.com",
    )
    if sign_contract_multi.prepare_url is not None:
        open_browser(sign_contract_multi.prepare_url)


if __name__ == "__main__":
    main()
