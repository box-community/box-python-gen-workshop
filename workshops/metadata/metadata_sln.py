""" Box Metadata exercises"""

import logging
from datetime import datetime
from typing import Dict, List

from box_sdk_gen import (
    AiResponseFull,
    BoxAPIError,
    CreateAiAskItems,
    CreateFileMetadataByIdScope,
    CreateMetadataTemplateFields,
    CreateMetadataTemplateFieldsOptionsField,
    CreateMetadataTemplateFieldsTypeField,
    MetadataTemplate,
    SearchByMetadataQueryOrderBy,
    SearchByMetadataQueryOrderByDirectionField,
    UpdateFileMetadataByIdRequestBody,
    UpdateFileMetadataByIdRequestBodyOpField,
    UpdateFileMetadataByIdScope,
)

from utils.box_ai_client_oauth import BoxAIClient, ConfigOAuth, get_ai_client_oauth
from utils.intelligence import ExtractStructuredMetadataTemplate

logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)

INVOICE_FOLDER = "261456614253"
PO_FOLDER = "261457585224"
ENTERPRISE_SCOPE = "enterprise_1134207681"


def get_template_by_key(client: BoxAIClient, template_key: str) -> MetadataTemplate:
    """Get a metadata template by key"""

    scope = "enterprise"

    try:
        template = client.metadata_templates.get_metadata_template(scope=scope, template_key=template_key)
    except BoxAPIError as err:
        if err.response_info.status_code == 404:
            template = None
        else:
            raise err

    return template


def delete_template_by_key(client: BoxAIClient, template_key: str):
    """Delete a metadata template by key"""

    scope = "enterprise"

    try:
        client.metadata_templates.delete_metadata_template(scope=scope, template_key=template_key)
    except BoxAPIError as err:
        if err.response_info.status_code == 404:
            pass
        else:
            raise err


def create_invoice_po_template(client: BoxAIClient, template_key: str, display_name: str) -> MetadataTemplate:
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
            key="vendor",
            display_name="Vendor",
            description="Vendor name or designation",
        )
    )

    # Invoice number
    fields.append(
        CreateMetadataTemplateFields(
            type=CreateMetadataTemplateFieldsTypeField.STRING,
            key="invoiceNumber",
            display_name="Invoice Number",
            description="Document number or associated invoice",
        )
    )

    # PO number
    fields.append(
        CreateMetadataTemplateFields(
            type=CreateMetadataTemplateFieldsTypeField.STRING,
            key="purchaseOrderNumber",
            display_name="Purchase Order Number",
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
    client_ai: BoxAIClient, file_id: str, scope: str, template_key: str
) -> AiResponseFull:
    """Get metadata suggestions for a file"""

    item = CreateAiAskItems(id=file_id, type="file")
    metadata_template = ExtractStructuredMetadataTemplate(scope=scope, template_key=template_key)
    return client_ai.intelligence.extract_structured(items=[item], metadata_template=metadata_template)


def convert_to_datetime(date_string):
    """
    Converts a date string in the format 'February 13, 2024' or '2024-03-13' to a datetime object.

    :param date_string: The date string to convert.
    :return: A datetime object or None if the format is not recognized.
    """
    # Define possible date formats
    date_formats = ["%B %d, %Y", "%Y-%m-%d"]

    for date_format in date_formats:
        try:
            # Attempt to parse the date string with the current format
            return datetime.strptime(date_string, date_format)
        except ValueError:
            # If parsing fails, continue to the next format
            continue

    # If none of the formats match, return None
    return None


def apply_template_to_file(client: BoxAIClient, file_id: str, template_key: str, data: Dict[str, str]):
    """Apply a metadata template to a folder"""
    default_data = {
        "documentType": "Unknown",
        "documentDate": "1900-01-01T00:00:00Z",
        "total": "Unknown",
        "vendor": "Unknown",
        "invoiceNumber": "Unknown",
        "purchaseOrderNumber": "Unknown",
    }

    # remove empty values
    data = {k: v for k, v in data.items() if v}

    # Check if data has a date
    if "documentDate" in data:
        try:
            date_string = data["documentDate"]
            date2 = convert_to_datetime(date_string)

            data["documentDate"] = date2.isoformat().replace("+00:00", "") + "Z"
        except ValueError as e:
            data["documentDate"] = "1900-01-01T00:00:00Z"
            print(f"Error converting date: {e}")

    # Merge the default data with the data
    data = {**default_data, **data}

    try:
        client.file_metadata.create_file_metadata_by_id(
            file_id=file_id,
            scope=CreateFileMetadataByIdScope.ENTERPRISE,
            template_key=template_key,
            request_body=data,
        )
    except BoxAPIError as error_a:
        if error_a.response_info.status_code == 409:
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
            except BoxAPIError as error_b:
                logging.error(f"Error updating metadata: {error_b.status}:{error_b.code}:{file_id}")
        else:
            raise error_a


def get_file_metadata(client: BoxAIClient, file_id: str, template_key: str):
    """Get file metadata"""
    metadata = client.file_metadata.get_file_metadata_by_id(
        file_id=file_id,
        scope=CreateFileMetadataByIdScope.ENTERPRISE,
        template_key=template_key,
    )
    return metadata


def search_metadata(
    client: BoxAIClient,
    template_key: str,
    folder_id: str,
    query: str,
    query_params: Dict[str, str],
    order_by: List[Dict[str, str]] = None,
):
    """Search for files with metadata"""

    from_ = ENTERPRISE_SCOPE + "." + template_key

    if order_by is None:
        order_by = [
            SearchByMetadataQueryOrderBy(
                field_key="invoiceNumber",
                direction=SearchByMetadataQueryOrderByDirectionField.ASC,
            )
        ]

    fields = [
        "type",
        "id",
        "name",
        "metadata." + from_ + ".invoiceNumber",
        "metadata." + from_ + ".purchaseOrderNumber",
    ]

    search_result = client.search.search_by_metadata_query(
        from_=from_,
        query=query,
        query_params=query_params,
        ancestor_folder_id=folder_id,
        order_by=order_by,
        fields=fields,
    )
    return search_result


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
            f"\nMetadata template created: {template.display_name} ",
            f"[{template.id}]",
        )
    else:
        # print("\nMetadata template does not exist, creating...")

        # create a metadata template
        template = create_invoice_po_template(client, template_key, template_display_name)
        print(
            f"\nMetadata template created: {template.display_name} ",
            f"[{template.id}]",
        )

    # # Scan the purchase folder for metadata suggestions
    folder_items = client.folders.get_folder_items(PO_FOLDER)
    for item in folder_items.entries:
        print(f"\nItem: {item.name} [{item.id}]")
        ai_response = get_metadata_suggestions_for_file(client, item.id, ENTERPRISE_SCOPE, template_key)
        print(f"Suggestions: {ai_response.answer}")
        metadata = ai_response.answer
        apply_template_to_file(
            client,
            item.id,
            template_key,
            metadata,
        )

    # # Scan the invoice folder for metadata suggestions
    folder_items = client.folders.get_folder_items(INVOICE_FOLDER)
    for item in folder_items.entries:
        print(f"\nItem: {item.name} [{item.id}]")
        ai_response = get_metadata_suggestions_for_file(client, item.id, ENTERPRISE_SCOPE, template_key)
        print(f"Suggestions: {ai_response.answer}")
        metadata = ai_response.answer
        apply_template_to_file(
            client,
            item.id,
            template_key,
            metadata,
        )

    # get metadata for a file
    metadata = get_file_metadata(client, folder_items.entries[0].id, template_key)
    print(f"\nMetadata for file: {metadata.extra_data}")

    # # search for invoices without purchase orders
    query = "documentType = :docType AND purchaseOrderNumber = :poNumber"
    query_params = {"docType": "Invoice", "poNumber": "Unknown"}

    search_result = search_metadata(client, template_key, INVOICE_FOLDER, query, query_params)
    print(f"\nSearch results: {search_result.entries}")

    # # delete the metadata template
    # delete_template_by_key(client, "rbInvoicePO")
    # print("\nMetadata template deleted")


if __name__ == "__main__":
    main()
