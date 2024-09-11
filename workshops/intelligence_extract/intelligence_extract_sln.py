import json
import logging
from typing import List, Optional

from box_sdk_gen import AiResponse, CreateAiAskItems

from utils.box_ai_client_oauth import BoxAIClient, ConfigOAuth, get_ai_client_oauth
from utils.intelligence import (
    ExtractStructuredField,
    ExtractStructuredFieldOption,
    ExtractStructuredMetadataTemplate,
)

logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)

SAMPLE_INVOICE = "1644174078580"


def intelligence_extract(client: BoxAIClient, file_id: str, prompt: str) -> AiResponse:
    items = CreateAiAskItems(id=file_id, type="file")

    # file = client.files.get_file_by_id(file_id)
    ai_response: AiResponse = client.intelligence.extract(prompt=prompt, items=[items])

    return ai_response


def intelligence_extract_structured(
    client: BoxAIClient,
    file_id: str,
    fields: Optional[List[ExtractStructuredField]] = None,
    metadata_template: Optional[ExtractStructuredMetadataTemplate] = None,
) -> AiResponse:
    items = CreateAiAskItems(id=file_id, type="file")

    # file = client.files.get_file_by_id(file_id)
    ai_response: AiResponse = client.intelligence.extract_structured(
        items=[items], fields=fields, metadata_template=metadata_template
    )

    return ai_response


def main():
    """Simple script to demonstrate how to use the Box SDK"""
    conf = ConfigOAuth()
    client = get_ai_client_oauth(conf)

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
    fields: List[ExtractStructuredField] = []

    fields.append(
        ExtractStructuredField(
            key="documentType",
            type="enum",
            prompt="what type of document is this?",
            options=[
                ExtractStructuredFieldOption(key="Invoice"),
                ExtractStructuredFieldOption(key="Purchase Order"),
                ExtractStructuredFieldOption(key="Unknown"),
            ],
        )
    )

    fields.append(
        ExtractStructuredField(
            key="doc_number",
            type="string",
            prompt="what is the document number?",
        )
    )

    fields.append(
        ExtractStructuredField(
            key="date",
            type="date",
            prompt="what is the date of the document?",
        )
    )

    fields.append(
        ExtractStructuredField(
            key="vendor",
            type="string",
            prompt="who is the vendor?",
        )
    )

    fields.append(
        ExtractStructuredField(
            key="total",
            type="float",
            prompt="what is the total amount?",
        )
    )

    fields.append(
        ExtractStructuredField(
            key="poNumber",
            type="string",
            prompt="what is the PO number?",
        )
    )

    ai_response = intelligence_extract_structured(client, SAMPLE_INVOICE, fields)
    print(f"Using Extract structured\nResponse: \n{ai_response.answer}")


if __name__ == "__main__":
    main()
