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

SIGNER_A = "YOUR_EMAIL+A@gmail.com"
SIGNER_A_PHONE = "+15554443322"

SIGNER_B = "YOUR_EMAIL+B@gmail.com"

APPROVER = "YOUR_EMAIL+APPROVER@gmail.com"
FINAL_COPY = "YOUR_EMAIL+FINAL_COPY@gmail.com"


def check_sign_request(sign_request: SignRequest):
    print(f"\nSimple sign request: {sign_request.id}")
    print(f"  Status: {sign_request.status.value}")
    print(f"  Signers: {sign_request.signers[0].email}")
    print(f"  Prepare url: {sign_request.prepare_url}")


def sign_doc_single(
    client: Client,
    document_id: str,
    destination_folder_id: str,
    signer_email: str,
    prep_needed: bool = False,
) -> SignRequest:
    """Single doc sign by single signer"""

    # Sign request params
    source_file = FileBase(id=document_id, type=FileBaseTypeField.FILE)
    destination_folder = FolderMini(
        id=destination_folder_id, type=FolderBaseTypeField.FOLDER
    )
    signer = SignRequestCreateSigner(signer_email)
    # sign document
    sign_request = client.sign_requests.create_sign_request(
        signers=[signer],
        parent_folder=destination_folder,
        source_files=[source_file],
        is_document_preparation_needed=prep_needed,
    )

    return sign_request


def sign_contract(
    client: Client,
    document_id: str,
    destination_folder_id: str,
    institution_email: str,
    student_email: str,
    prep_needed: bool = False,
) -> SignRequest:
    """Sign contract"""

    # Sign request params
    source_file = FileBase(id=document_id, type=FileBaseTypeField.FILE)
    destination_folder = FolderMini(
        id=destination_folder_id, type=FolderBaseTypeField.FOLDER
    )

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
        parent_folder=destination_folder,
        source_files=[source_file],
        is_document_preparation_needed=prep_needed,
    )

    return sign_request


def sign_send_reminder(client: Client, sign_request_id: str):
    """Send reminder to signers"""
    sign_request = client.sign_requests.resend_sign_request(sign_request_id)
    return sign_request


def sign_doc_single_more_options(
    client: Client,
    document_id: str,
    destination_folder_id: str,
    signer_email: str,
    prep_needed: bool = False,
    auto_reminder: bool = False,
    days_valid: int = None,
    redirect_url: str = None,
    declined_redirect_url: str = None,
    email_subject: str = None,
    email_message: str = None,
) -> SignRequest:
    """Single doc sign by single signer"""

    # Sign request params
    source_file = FileBase(id=document_id, type=FileBaseTypeField.FILE)
    destination_folder = FolderMini(
        id=destination_folder_id, type=FolderBaseTypeField.FOLDER
    )

    # signer
    signer = SignRequestCreateSigner(signer_email)

    # sign document
    sign_request = client.sign_requests.create_sign_request(
        signers=[signer],
        parent_folder=destination_folder,
        source_files=[source_file],
        is_document_preparation_needed=prep_needed,
        are_reminders_enabled=auto_reminder,
        days_valid=days_valid,
        redirect_url=redirect_url,
        declined_redirect_url=declined_redirect_url,
        email_subject=email_subject,
        email_message=email_message,
    )

    return sign_request


def sign_doc_verify_phone(
    client: Client,
    document_id: str,
    destination_folder_id: str,
    signer_email: str,
    signer_phone: str,
) -> SignRequest:
    # Sign request params
    source_file = FileBase(id=document_id, type=FileBaseTypeField.FILE)
    destination_folder = FolderMini(
        id=destination_folder_id, type=FolderBaseTypeField.FOLDER
    )

    signer = SignRequestCreateSigner(
        email=signer_email,
        verification_phone_number=signer_phone,
    )

    # sign document
    sign_request = client.sign_requests.create_sign_request(
        signers=[signer],
        parent_folder=destination_folder,
        source_files=[source_file],
        is_phone_verification_required_to_view=True,
    )

    return sign_request


def sign_doc_verify_password(
    client: Client,
    document_id: str,
    destination_folder_id: str,
    signer_email: str,
    signer_password: str,
) -> SignRequest:
    # Sign request params
    source_file = FileBase(id=document_id, type=FileBaseTypeField.FILE)
    destination_folder = FolderMini(
        id=destination_folder_id, type=FolderBaseTypeField.FOLDER
    )

    # signer
    signer = SignRequestCreateSigner(
        email=signer_email,
        password=signer_password,
    )

    # sign document
    sign_request = client.sign_requests.create_sign_request(
        signers=[signer],
        parent_folder=destination_folder,
        source_files=[source_file],
    )

    return sign_request


def sign_contract_step(
    client: Client,
    document_id: str,
    destination_folder_id: str,
    institution_email: str,
    student_email: str,
    dean_email: str,
    legal_email: str,
) -> SignRequest:
    """Sign contract"""

    # Sign request params
    source_file = FileBase(id=document_id, type=FileBaseTypeField.FILE)
    destination_folder = FolderMini(
        id=destination_folder_id, type=FolderBaseTypeField.FOLDER
    )

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

    dean = SignRequestCreateSigner(
        email=dean_email,
        role=SignRequestCreateSignerRoleField.APPROVER,
    )

    legal = SignRequestCreateSigner(
        email=legal_email,
        role=SignRequestCreateSignerRoleField.FINAL_COPY_READER,
    )

    # create sign request
    sign_request = client.sign_requests.create_sign_request(
        signers=[institution, student, dean, legal],
        parent_folder=destination_folder,
        source_files=[source_file],
        is_document_preparation_needed=True,
    )

    return sign_request


def main():
    """Simple script to demonstrate how to use the Box SDK"""
    conf = ConfigOAuth()
    client = get_client_oauth(conf)

    # user = client.users.get_user_me()
    # print(f"\nHello, I'm {user.name} ({user.login}) [{user.id}]")

    # # Simple sign a pdf request
    # sign_pdf = sign_doc_single(client, SIMPLE_PDF, SIGN_DOCS_FOLDER, SIGNER_A)
    # check_sign_request(sign_pdf)

    # Simple sign a pdf request with preparation
    sign_pdf_prep = sign_doc_single(
        client, SIMPLE_PDF, SIGN_DOCS_FOLDER, SIGNER_A, True
    )
    check_sign_request(sign_pdf_prep)
    if sign_pdf_prep.prepare_url is not None:
        open_browser(sign_pdf_prep.prepare_url)

    # # Multiple signers
    # sign_contract_multi = sign_contract(
    #     client,
    #     CONTRACT,
    #     SIGN_DOCS_FOLDER,
    #     institution_email=SIGNER_A,
    #     student_email=SIGNER_B,
    #     prep_needed=True,
    # )
    # if sign_contract_multi.prepare_url is not None:
    #     open_browser(sign_contract_multi.prepare_url)

    # # Send the original request
    # sign_pdf_resend = sign_doc_single(
    #     client, SIMPLE_PDF, SIGN_DOCS_FOLDER, SIGNER_A
    # )
    # check_sign_request(sign_pdf_resend)

    # # Resend the request
    # sign_send_reminder(client, sign_pdf_resend.id)
    # check_sign_request(sign_pdf_resend)

    # # Sign with redirects
    # sign_with_redirects = sign_doc_single_more_options(
    #     client,
    #     SIMPLE_PDF,
    #     SIGN_DOCS_FOLDER,
    #     SIGNER_A,
    #     prep_needed=False,
    #     redirect_url="https://forum.box.com/",
    #     declined_redirect_url="https://developer.box.com/",
    # )
    # check_sign_request(sign_with_redirects)

    # # Sign with custom email subject
    # sign_custom_email_subject = sign_doc_single_more_options(
    #     client,
    #     SIMPLE_PDF,
    #     SIGN_DOCS_FOLDER,
    #     SIGNER_A,
    #     prep_needed=False,
    #     email_subject="All we need is your signature to get started",
    # )
    # check_sign_request(sign_custom_email_subject)

    # # Sign with phone verification
    # sign_with_phone_verification = sign_doc_verify_phone(
    #     client,
    #     SIMPLE_PDF,
    #     SIGN_DOCS_FOLDER,
    #     SIGNER_A,
    #     SIGNER_A_PHONE,
    # )
    # check_sign_request(sign_with_phone_verification)

    # # Sign with phone verification
    # sign_with_password_verification = sign_doc_verify_password(
    #     client,
    #     SIMPLE_PDF,
    #     SIGN_DOCS_FOLDER,
    #     SIGNER_A,
    #     "1234",
    # )
    # check_sign_request(sign_with_password_verification)

    # # Multiple signers and steps
    # sign_contract_multi_step = sign_contract_step(
    #     client,
    #     CONTRACT,
    #     SIGN_DOCS_FOLDER,
    #     institution_email=SIGNER_A,
    #     student_email=SIGNER_B,
    #     dean_email=APPROVER,
    #     legal_email=FINAL_COPY,
    # )
    # if sign_contract_multi_step.prepare_url is not None:
    #     open_browser(sign_contract_multi_step.prepare_url)


if __name__ == "__main__":
    main()
