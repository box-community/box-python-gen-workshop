# Metadata



## Pre-requisites


## Concepts



References to our documentation:
* 

# Exercises
## Setup
Create a `metadata_init.py` file on the root of the project and execute the following code:
```python
"""upload sample content to box"""
import logging
from utils.box_client_oauth import ConfigOAuth, get_client_oauth

from workshops.metadata.create_samples import upload_content_sample

logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)

conf = ConfigOAuth()


def main():
    client = get_client_oauth(conf)
    upload_content_sample(client)


if __name__ == "__main__":
    main()

```
Result:
```yaml
INFO:root:Folder workshops with id: 248851586376
INFO:root:Folder metadata with id: 248847004564
INFO:root:Folder invoices with id: 248846701954
INFO:root: Folder invoices
INFO:root:      Uploaded Invoice-Q8888.txt (1443478591184) 158 bytes
INFO:root:      Uploaded Invoice-B1234.txt (1443446103636) 162 bytes
INFO:root:      Uploaded Invoice-C9876.txt (1443455423129) 183 bytes
INFO:root:      Uploaded Invoice-A5555.txt (1443449154029) 170 bytes
INFO:root:      Uploaded Invoice-Q2468.txt (1443455656177) 170 bytes
INFO:root:      Uploaded Invoice-W9999.txt (1443450068472) 173 bytes
INFO:root:      Uploaded Invoice-N7777.txt (1443446363085) 182 bytes
INFO:root:      Uploaded Invoice-N3333.txt (1443478787777) 147 bytes
INFO:root:      Uploaded Invoice-C1111.txt (1443478857049) 156 bytes
INFO:root:      Uploaded Invoice-A2222.txt (1443477560466) 160 bytes
INFO:root:Folder purchase_orders with id: 248852070443
INFO:root: Folder purchase_orders
INFO:root:      Uploaded PO-008.txt (1443446236634) 202 bytes
INFO:root:      Uploaded PO-009.txt (1443452445097) 183 bytes
INFO:root:      Uploaded PO-001.txt (1443479464395) 195 bytes
INFO:root:      Uploaded PO-002.txt (1443447637477) 212 bytes
INFO:root:      Uploaded PO-003.txt (1443452989216) 205 bytes
INFO:root:      Uploaded PO-007.txt (1443477075692) 193 bytes
INFO:root:      Uploaded PO-006.txt (1443455828977) 216 bytes
INFO:root:      Uploaded PO-010.txt (1443480075910) 188 bytes
INFO:root:      Uploaded PO-004.txt (1443453421426) 200 bytes
INFO:root:      Uploaded PO-005.txt (1443454854559) 194 bytes
```

Next, create a `metadata.py` file on the root of the project that you will use to write your code.

```python

```

Resulting in:

```yaml
Hello, I'm Rui Barbosa (barduinor@gmail.com) [18622116055]
```
## Create some helper functions
To make our life easier later, let's create some helper functions to interact with the Box API.

First, let's create a function to get a template by key:

```python
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
```

Next, let's create a function to delete a template by key, just in case you get stuck and need to start over:

```python
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
```

## Create a metadata template

To be able to work with metadata we need a metadata template to define the metadata fields we want to use. 
Because metadata templates are common to the entire enterprise, use your initials as a prefix to the template key to avoid conflicts with other users.

Let's create a metadata template using this method:
```python
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
            description="Identifies document as an invoice or purchase order",
            options=[
                CreateMetadataTemplateFieldsOptionsField(key="Invoice"),
                CreateMetadataTemplateFieldsOptionsField(key="Purchase Order"),
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
            type=CreateMetadataTemplateFieldsTypeField.FLOAT,
            key="documentTotal",
            display_name="Document Total",
            description="Total USD value of document",
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
            key="invoice",
            display_name="Invoice #",
            description="Document number or associated invoice",
        )
    )

    # PO number
    fields.append(
        CreateMetadataTemplateFields(
            type=CreateMetadataTemplateFieldsTypeField.STRING,
            key="po",
            display_name="PO #",
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
```

In the main function, let's check if the template already exists and if not, create it.

>Remember to update the template key and display name to match your initials.

```python
def main():
    ...

    # check if template exists
    template_key = "rbInvoicePO"
    template_display_name = "RB: Invoice & POs"
    template = get_template_by_key(client, template_key)

    if template:
        print(
            f"\nMetadata template exists: '{template.display_name}' ",
            f"[{template.id}]",
        )
    else:
        print("\nMetadata template does not exist, creating...")

        # create a metadata template
        template = create_invoice_po_template(
            client, template_key, template_display_name
        )
        print(
            f"\nMetadata template created: '{template.display_name}' ",
            f"[{template.id}]",
        )
```    
This results in:
```yaml
Hello, I'm Rui Barbosa (anovotny+rbarbosa@boxdemo.com) [31699333422]
Metadata template does not exist, creating...
Metadata template created: 'RB: Invoice & POs'  [2257ed5b-c4c3-48b1-9881-875b5291ddfa]
```

If you run the code again, you should see the message that the template already exists.
```yaml
Metadata template exists: 'RB: Invoice & POs'  [2257ed5b-c4c3-48b1-9881-875b5291ddfa]
```

## Scanning the content using the metadata suggestions
Now let's see what are the metadata suggestions for the purchase orders.


## Updating the content metadata

## Finding unmatched invoices

## Extra credit
* 

## Final thoughts









