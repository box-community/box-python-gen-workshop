import logging
import random
from datetime import date, datetime
from time import sleep
from typing import List

from box_sdk_gen import (
    BoxClient,
    CreateDocgenBatchV2025R0DestinationFolder,
    DocGenBatchBaseV2025R0,
    DocGenDocumentGenerationDataV2025R0,
    DocGenTemplateV2025R0,
    FileBaseTypeField,
    FileMini,
    FileReferenceV2025R0,
    FolderBaseTypeField,
    FolderMini,
    SignRequest,
    SignRequestCreateSigner,
)
from dateutil.relativedelta import relativedelta

from utils.box_client_oauth import ConfigOAuth, get_client_oauth

logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)

LEASE_TEMPLATE_ID = "1744637428174"
LEASES_FOLDER_ID = "301836779172"
SIGNED_LEASES_FOLDER_ID = "301990449099"


def set_file_as_template(client: BoxClient, file_id: str) -> DocGenTemplateV2025R0:
    """Mark a file as a DocGen template"""
    # check if file exists and it is accessible
    file = client.files.get_file_by_id(file_id)

    template_base = client.docgen_template.create_docgen_template_v2025_r0(
        file=FileReferenceV2025R0(id=file.id)
    )
    return client.docgen_template.get_docgen_template_by_id_v2025_r0(
        template_base.file.id
    )


def generate_new_data(
    name: str, email: str, start_date: date
) -> DocGenDocumentGenerationDataV2025R0:
    # gen random property id
    property = f"HAB-2-{random.randint(1000, 9999):04}"
    # todays date
    lease_date = date.today()
    # end date in 3 years
    end_date = start_date + relativedelta(years=3)

    return DocGenDocumentGenerationDataV2025R0(
        generated_file_name=f"{property}.pdf",
        user_input={
            "LeaseDate": lease_date.isoformat(),
            "Tenant": name,
            "Email": email,
            "PropertyType": "Dual Residential Pod",
            "Property": property,
            "Description": "Two private and spacious bedrooms, each equipped with a temperature-regulating system, offering breathtaking views of the lunar landscape through reinforced transparent panels. Bedrooms are fitted with built-in storage for personal items and lunar suits.",
            "StartDate": start_date.isoformat(),
            "EndDate": end_date.isoformat(),
            "Rent": f"${5535:,.2f}",
        },
    )


def generate_new_document(
    client: BoxClient,
    template_id: str,
    destination_folder_id: str,
    data: List[DocGenDocumentGenerationDataV2025R0],
) -> DocGenBatchBaseV2025R0:
    """Generate a new document from a template"""
    template_file = FileReferenceV2025R0(id=template_id)
    destination_folder = CreateDocgenBatchV2025R0DestinationFolder(
        id=destination_folder_id
    )
    return client.docgen.create_docgen_batch_v2025_r0(
        file=template_file,
        input_source="api",
        destination_folder=destination_folder,
        output_type="pdf",
        document_generation_data=data,
    )


def create_sign_request_structured(
    client: BoxClient, file_id: str, tenant_email: str, landlord_email: str
) -> SignRequest:
    """Create a sign request with structured data"""

    # Sign request params
    structure_file = FileMini(id=file_id, type=FileBaseTypeField.FILE)
    parent_folder = FolderMini(
        id=SIGNED_LEASES_FOLDER_ID, type=FolderBaseTypeField.FOLDER
    )
    landlord_signer = SignRequestCreateSigner(email=landlord_email, order=1)
    tenant_signer = SignRequestCreateSigner(email=tenant_email, order=2)

    # Create a sign request
    sign_request = client.sign_requests.create_sign_request(
        signers=[landlord_signer, tenant_signer],
        parent_folder=parent_folder,
        source_files=[structure_file],
    )

    return sign_request


def main():
    """Simple script to demonstrate how to use the Box SDK"""
    conf = ConfigOAuth()
    client = get_client_oauth(conf)

    me = client.users.get_user_me()
    print(f"\nHello, I'm {me.name} ({me.login}) [{me.id}]")
    print("-" * 50)
    print()

    # Set the MS Word file as a doc gen template
    template = set_file_as_template(client, LEASE_TEMPLATE_ID)
    print(f"Template created: {template.to_dict()}")

    # List template tags
    template_tags = client.docgen_template.get_docgen_template_tags_v2025_r0(
        template_id=template.file.id
    )
    print("\nFound tags:")
    for tag in template_tags.entries:
        print(f"  - {tag.tag_content} : {tag.tag_type.name} : {tag.json_paths}")

    # Generate 5 new lease agreement
    docs_data: List[DocGenDocumentGenerationDataV2025R0] = []
    start_date = date.today().replace(day=1) + relativedelta(months=1)

    # Create 5 random person names
    persons = ["John Doe", "Jane Doe", "Alice Smith", "Bob Johnson", "Eve Brown"]

    for person in persons:
        lease_data = generate_new_data(
            name=person,
            email=f"{person.replace(' ', '.').lower()}@example.com",
            start_date=start_date,
        )
        docs_data.append(lease_data)

    batch = generate_new_document(client, template.file.id, LEASES_FOLDER_ID, docs_data)
    print(f"\nNew batch created: {batch.to_dict()}")

    # Get jobs in batch
    print("\nJobs in batch:")
    jobs = client.docgen.get_docgen_batch_job_by_id_v2025_r0(batch.id)
    for job in jobs.entries:
        print(f"  - Job {job.id} - {job.status.name}")

    # List jobs in batch
    print("\nJob details:")
    for job in jobs.entries:
        job_details = client.docgen.get_docgen_job_by_id_v2025_r0(job.id)
        print(f"  - {job_details.to_dict()}\n")
        sleep(3)

    # List all jobs for user
    user_jobs = client.docgen.get_docgen_jobs_v2025_r0(limit=5)
    print("\nAll jobs for current user:")
    for job in user_jobs.entries:
        print(
            f"  - Job {job.id} {datetime.fromtimestamp(int(job.created_at)).isoformat()} {job.status.name}"
        )

    # List all jobs by template
    template_jobs = client.docgen_template.get_docgen_template_job_by_id_v2025_r0(
        template.file.id, limit=5
    )
    print("\nAll jobs for template:")
    for job in template_jobs.entries:
        print(
            f"  - Job {job.id} {datetime.fromtimestamp(int(job.created_at)).isoformat()} {job.status.name}"
        )

    # Remove the template
    client.docgen_template.delete_docgen_template_by_id_v2025_r0(template.file.id)

    # List all templates
    templates = client.docgen_template.get_docgen_templates_v2025_r0()
    print("\nAll templates:")

    if templates.entries:
        for template in templates.entries:
            print(f"  - {template.to_dict()}")
    else:
        print("  - No templates found")

    # Request signature for first lease
    sign_job = client.docgen.get_docgen_job_by_id_v2025_r0(jobs.entries[0].id)
    sign_request = create_sign_request_structured(
        client,
        sign_job.output_file.id,
        tenant_email="YOUR_TENANT_EMAIL@example.com",
        landlord_email="YOUR_LANDLORD_EMAIL@example.com",
    )
    print(f"\nSign request created: {sign_request.to_dict()}")


if __name__ == "__main__":
    main()
