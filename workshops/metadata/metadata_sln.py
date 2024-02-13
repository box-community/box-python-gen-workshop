""" Metadata Box exercises"""

import logging
from typing import Dict


from utils.box_ai_client import BoxAIClient as Client
from box_sdk_gen.fetch import APIException

from box_sdk_gen.schemas import MetadataTemplate
from utils.ai_schemas import IntelligenceMetadataSuggestions
from box_sdk_gen.managers.metadata_templates import (
    CreateMetadataTemplateFields,
    CreateMetadataTemplateFieldsTypeField,
    CreateMetadataTemplateFieldsOptionsField,
)


from box_sdk_gen.managers.file_metadata import (
    CreateFileMetadataByIdScope,
    UpdateFileMetadataByIdScope,
    UpdateFileMetadataByIdRequestBody,
    UpdateFileMetadataByIdRequestBodyOpField,
)

from utils.box_ai_client_oauth import ConfigOAuth, get_ai_client_oauth

logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)

INVOICE_FOLDER = "248887218023"
PO_FOLDER = "248891043873"
ENTERPRISE_SCOPE = "enterprise_1133807781"


def get_template_by_key(client: Client, template_key: str) -> MetadataTemplate:
    """Get a metadata template by key"""

    scope = "enterprise"

    try:
        template = client.metadata_templates.get_metadata_template(
            scope=scope, template_key=template_key
        )
    except APIException as e:
        if e.status == 404:
            template = None
        else:
            raise e

    return template


def delete_template_by_key(client: Client, template_key: str):
    """Delete a metadata template by key"""

    scope = "enterprise"

    try:
        client.metadata_templates.delete_metadata_template(
            scope=scope, template_key=template_key
        )
    except APIException as e:
        if e.status == 404:
            pass
        else:
            raise e


def create_invoice_po_template(
    client: Client, template_key: str, display_name: str
) -> MetadataTemplate:
    """Create a metadata template"""

    scope = "enterprise"

    fields = []

    # Document type
    fields.append(
        CreateMetadataTemplateFields(
            type=CreateMetadataTemplateFieldsTypeField.ENUM,
            key="documentType",
            display_name="Document Type",
            options=[
                CreateMetadataTemplateFieldsOptionsField(key="Invoice"),
                CreateMetadataTemplateFieldsOptionsField(key="Purchase Order"),
                CreateMetadataTemplateFieldsOptionsField(key="Unknown"),
            ],
        )
    )

    # Date
    fields.append(
        CreateMetadataTemplateFields(
            type=CreateMetadataTemplateFieldsTypeField.DATE,
            key="documentDate",
            display_name="Document Date",
        )
    )

    # Document total
    fields.append(
        CreateMetadataTemplateFields(
            type=CreateMetadataTemplateFieldsTypeField.STRING,
            key="total",
            display_name="Total: $",
            description="Total: $",
        )
    )

    # Supplier
    fields.append(
        CreateMetadataTemplateFields(
            type=CreateMetadataTemplateFieldsTypeField.STRING,
            key="supplier",
            display_name="Supplier",
            description="Supplier name or designation",
        )
    )

    # Invoice number
    fields.append(
        CreateMetadataTemplateFields(
            type=CreateMetadataTemplateFieldsTypeField.STRING,
            key="invoice",
            display_name="Invoice #",
            description="Document number or associated invoice",
        )
    )

    # PO number
    fields.append(
        CreateMetadataTemplateFields(
            type=CreateMetadataTemplateFieldsTypeField.STRING,
            key="purchaseOrder",
            display_name="Purchase Order #",
            description="Document number or associated purchase order",
        )
    )

    template = client.metadata_templates.create_metadata_template(
        scope=scope,
        template_key=template_key,
        display_name=display_name,
        fields=fields,
    )

    return template


def get_metadata_suggestions_for_file(
    client: Client, file_id: str, enterprise_scope: str, template_key: str
) -> IntelligenceMetadataSuggestions:
    """Get metadata suggestions for a file"""
    return client.intelligence.intelligence_metadata_suggestion(
        item=file_id,
        scope=enterprise_scope,
        template_key=template_key,
        confidence="experimental",
    )


def apply_template_to_file(
    client: Client, file_id: str, template_key: str, data: Dict[str, str]
):
    """Apply a metadata template to a folder"""
    default_data = {
        "documentType": "Unknown",
        "documentDate": "1900-01-01T00:00:00Z",
        "total": "Unknown",
        "supplier": "Unknown",
        "invoice": "Unknown",
        "purchaseOrder": "Unknown",
    }
    # Merge the default data with the data
    data = {**default_data, **data}

    try:
        client.file_metadata.create_file_metadata_by_id(
            file_id=file_id,
            scope=CreateFileMetadataByIdScope.ENTERPRISE,
            template_key=template_key,
            request_body=data,
        )
    except APIException as e:
        if e.status == 409:
            # Update the metadata
            update_data = []
            for key, value in data.items():
                update_item = UpdateFileMetadataByIdRequestBody(
                    op=UpdateFileMetadataByIdRequestBodyOpField.ADD,
                    path=f"/{key}",
                    value=value,
                )
                update_data.append(update_item)
            try:
                client.file_metadata.update_file_metadata_by_id(
                    file_id=file_id,
                    scope=UpdateFileMetadataByIdScope.ENTERPRISE,
                    template_key=template_key,
                    request_body=update_data,
                )
            except APIException as e:
                print(
                    f"Error updating metadata: {e.status}:{e.code}:{file_id}"
                )
                print(f"Error updating metadata: {update_data}")
        else:
            raise e


def main():
    conf = ConfigOAuth()
    client = get_ai_client_oauth(conf)

    user = client.users.get_user_me()
    print(f"\nHello, I'm {user.name} ({user.login}) [{user.id}]")

    # check if template exists
    template_key = "rbInvoicePO"
    template_display_name = "RB: Invoice & POs"
    template = get_template_by_key(client, template_key)

    if template:
        print(
            f"\nMetadata template exists: {template.display_name} ",
            f"[{template.id}]",
        )
    else:
        print("\nMetadata template does not exist, creating...")

        # create a metadata template
        template = create_invoice_po_template(
            client, template_key, template_display_name
        )
        print(
            f"\nMetadata template created: {template.display_name} ",
            f"[{template.id}]",
        )

    # Scan the purchase folder for metadata suggestions
    folder_items = client.folders.get_folder_items(PO_FOLDER)
    for item in folder_items.entries:
        print(f"\nItem: {item.name} [{item.id}]")
        suggestions = get_metadata_suggestions_for_file(
            client, item.id, ENTERPRISE_SCOPE, template_key
        )
        print(f"Suggestions: {suggestions.suggestions}")
        metadata = suggestions.suggestions
        apply_template_to_file(
            client,
            item.id,
            template_key,
            metadata,
        )

    # Scan the invoice folder for metadata suggestions
    folder_items = client.folders.get_folder_items(INVOICE_FOLDER)
    for item in folder_items.entries:
        print(f"\nItem: {item.name} [{item.id}]")
        suggestions = get_metadata_suggestions_for_file(
            client, item.id, ENTERPRISE_SCOPE, template_key
        )
        print(f"Suggestions: {suggestions.suggestions}")
        metadata = suggestions.suggestions
        apply_template_to_file(
            client,
            item.id,
            template_key,
            metadata,
        )

    # delete the metadata template
    # delete_template_by_key(client, "rbInvoicePO")
    # print("\nMetadata template deleted")


if __name__ == "__main__":
    main()
