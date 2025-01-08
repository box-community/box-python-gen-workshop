import logging
import random
from datetime import date
from time import sleep
from typing import List

from box_sdk_gen import (
    BoxClient,
    CreateDocgenBatchDestinationFolder,
    CreateDocgenBatchFile,
    CreateDocgenTemplateFile,
    DocgenBatchBase,
    DocgenDocumentGenerationData,
    DocgenTags,
    DocgenTemplate,
)
from dateutil.relativedelta import relativedelta

from utils.box_client_oauth import ConfigOAuth, get_client_oauth

logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)

LEASE_TEMPLATE_ID = "1744637428174"
LEASES_FOLDER_ID = "301836779172"


def mark_file_as_doc_gen_template(client: BoxClient, file_id: str) -> DocgenTemplate:
    """Mark a file as a DocGen template"""
    # check if file exists and it is accessible
    file = client.files.get_file_by_id(file_id)

    template_base = client.doc_gen_template.create_docgen_template(file=CreateDocgenTemplateFile(id=file.id))
    return client.doc_gen_template.get_docgen_template_by_id(template_base.file.id)


def get_tags_from_template(client: BoxClient, template_id: str) -> DocgenTags:
    """Get tags from a template"""
    return client.doc_gen_template.get_docgen_template_tags(template_id)


def generate_new_document(
    client: BoxClient, template_id: str, destination_folder_id: str, data: List[DocgenDocumentGenerationData]
) -> DocgenBatchBase:
    """Generate a new document from a template"""
    template_file = CreateDocgenBatchFile(id=template_id)
    destination_folder = CreateDocgenBatchDestinationFolder(id=destination_folder_id)
    return client.doc_gen.create_docgen_batch(
        file=template_file,
        input_source="api",
        destination_folder=destination_folder,
        output_type="pdf",
        document_generation_data=data,
    )


def generate_new_data(name: str, email: str, start_date: date) -> DocgenDocumentGenerationData:
    # gen random property id
    property = f"HAB-2-{random.randint(1000, 9999):04}"
    # todays date
    lease_date = date.today()
    # end date in 3 years
    end_date = start_date + relativedelta(years=3)

    return DocgenDocumentGenerationData(
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
            "Rent": "5535",
        },
    )


def main():
    """Simple script to demonstrate how to use the Box SDK"""
    conf = ConfigOAuth()
    client = get_client_oauth(conf)

    me = client.users.get_user_me()
    print(f"\nHello, I'm {me.name} ({me.login}) [{me.id}]")
    print("-" * 50)
    print()

    # Set the MS Word file as a doc gen template
    template = mark_file_as_doc_gen_template(client, LEASE_TEMPLATE_ID)
    print(f"Template created: {template.to_dict()}")

    # List template tags
    template_tags = get_tags_from_template(client, template.file.id)
    print("\nFound tags:")
    for tag in template_tags.entries:
        print(f"  - {tag.tag_content} : {tag.tag_type.name} : {tag.json_paths}")

    # Generate a new lease agreement
    docs_data: List[DocgenDocumentGenerationData] = []
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

    # get jobs in batch
    jobs = client.doc_gen.get_docgen_batch_job_by_id(batch.id)
    for job in jobs.entries:
        print(f"Job {job.id} - {job.status.name}")
    sleep(10)
    print("\nAfter 10 seconds:")
    jobs = client.doc_gen.get_docgen_batch_job_by_id(batch.id)
    for job in jobs.entries:
        print(f"Job {job.id} - {job.status.name}")


if __name__ == "__main__":
    main()
