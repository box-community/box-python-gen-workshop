import json
import logging
from typing import List, Optional

from box_sdk_gen import (
    AiItemBase,
    AiResponse,
    AiResponseFull,
    CreateAiExtractStructuredFields,
    CreateAiExtractStructuredFieldsOptionsField,
    CreateAiExtractStructuredMetadataTemplate,
)

from utils.box_client_oauth import BoxClient, ConfigOAuth, get_client_oauth

logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)

SAMPLE_INVOICE = "1644174078580"


def intelligence_extract(client: BoxClient, file_id: str, prompt: str) -> AiResponse:
    items = AiItemBase(id=file_id, type="file")

    # file = client.files.get_file_by_id(file_id)
    ai_response: AiResponse = client.ai.create_ai_extract(prompt=prompt, items=[items])

    return ai_response


def intelligence_extract_structured(
    client: BoxClient,
    file_id: str,
    fields: Optional[List[CreateAiExtractStructuredFields]] = None,
    metadata_template: Optional[CreateAiExtractStructuredMetadataTemplate] = None,
) -> AiResponseFull:
    items = AiItemBase(id=file_id, type="file")

    # file = client.files.get_file_by_id(file_id)
    ai_response: AiResponseFull = client.ai.create_ai_extract_structured(
        items=[items], fields=fields, metadata_template=metadata_template
    )

    return ai_response


def main():
    """Simple script to demonstrate how to use the Box SDK"""
    conf = ConfigOAuth()
    client = get_client_oauth(conf)

    me = client.users.get_user_me()
    print(f"\nHello, I'm {me.name} ({me.login}) [{me.id}]")
    print("-" * 50)
    print()

    # Using a plain english prompt
    prompt = "find the document type (invoice or po), document number, date, vendor, total, and po number"
    ai_response = intelligence_extract(client, SAMPLE_INVOICE, prompt)
    print(f"Prompt: {prompt}\nResponse: \n{ai_response.answer}\n")

    # Using a more explicit prompt
    prompt = '{"document_type","document_number","date","vendor","total","PO"}'
    ai_response = intelligence_extract(client, SAMPLE_INVOICE, prompt)
    print(f"Prompt: {prompt}\nResponse: \n{ai_response.answer}\n")

    # Using a formal structure dictionary
    # converted to a JSON string prompt
    # to specify the fields
    my_structure = {
        "fields": [
            {"key": "documentType", "type": "string"},
            {"key": "doc_number", "type": "string"},
            {"key": "date", "type": "date"},
            {"key": "vendor", "type": "string"},
            {"key": "total", "type": "float"},
            {"key": "poNumber", "type": "string"},
        ]
    }
    prompt = json.dumps(my_structure, indent=2)
    ai_response = intelligence_extract(client, SAMPLE_INVOICE, prompt)
    print(f"Prompt: {prompt}\nResponse: \n{ai_response.answer}\n")

    # Extract structured endpoint
    fields: List[CreateAiExtractStructuredFields] = []

    fields.append(
        CreateAiExtractStructuredFields(
            key="documentType",
            type="enum",
            prompt="what type of document is this?",
            options=[
                CreateAiExtractStructuredFieldsOptionsField(key="Invoice"),
                CreateAiExtractStructuredFieldsOptionsField(key="Purchase Order"),
                CreateAiExtractStructuredFieldsOptionsField(key="Unknown"),
            ],
        )
    )

    fields.append(
        CreateAiExtractStructuredFields(
            key="doc_number",
            type="string",
            prompt="what is the document number?",
        )
    )

    fields.append(
        CreateAiExtractStructuredFields(
            key="date",
            type="date",
            prompt="what is the date of the document?",
        )
    )

    fields.append(
        CreateAiExtractStructuredFields(
            key="vendor",
            type="string",
            prompt="who is the vendor?",
        )
    )

    fields.append(
        CreateAiExtractStructuredFields(
            key="total",
            type="float",
            prompt="what is the total amount?",
        )
    )

    fields.append(
        CreateAiExtractStructuredFields(
            key="poNumber",
            type="string",
            prompt="what is the PO number?",
        )
    )

    ai_response_structured = intelligence_extract_structured(client, SAMPLE_INVOICE, fields)
    print(f"Using Extract structured\nResponse: \n{ai_response_structured.to_dict()}")


if __name__ == "__main__":
    main()
