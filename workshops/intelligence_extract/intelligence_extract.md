# Box AI Extract
This workshop explores the new extract endpoints of the Box AI platform, allowing you to query an unstructured document and get back structured data. This feature is especially valuable when you need to seamlessly send structured data to other systems.

## Pre-requisites
The Box AI extract API hasn't been official released yet, and it is currently undergoing a public beta.
To complete this workshop you will need to have a Box application specifically enabled for the Box AI API, only available to Enterprise Plus customers.

## Concepts
This API has 2 endpoints, and both return structured data from a document:
* `/ai/extract/` - You specify a less formal output structure, and the API will return the data in that format as best it can.
* `/ai/extract_structured/` - You specify a formal output structure, and the API will return the data in that specific format.

## Box AI documentation
This API doesn't have a public documentation yet, stay tunned for updates.

# Exercises
## Setup
Create a `intelligence_extract_init.py` file on the root of the project and execute the following code:
```python
"""create sample content to box"""

import logging
from utils.box_client_oauth import ConfigOAuth, get_client_oauth

from workshops.intelligence.create_samples import create_samples

logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)

conf = ConfigOAuth()


def main():
    client = get_client_oauth(conf)
    create_samples(client)


if __name__ == "__main__":
    main()

```
Result:
```yaml
INFO:root:Folder workshops with id: 260937698360
INFO:root:Folder intelligence with id: 260938146404
INFO:root:Folder invoices with id: 284233583732
INFO:root: Folder invoices
INFO:root:      Uploaded Invoice-Q8888.txt (1644195825091) 185 bytes
INFO:root:      Uploaded Invoice-B1234.txt (1644174078580) 189 bytes
INFO:root:      Uploaded Invoice-C9876.txt (1644175506127) 210 bytes
INFO:root:      Uploaded Invoice-A5555.txt (1644184002872) 171 bytes
INFO:root:      Uploaded Invoice-Q2468.txt (1644178304809) 197 bytes
INFO:root:Folder purchase_orders with id: 284230988983
INFO:root: Folder purchase_orders
INFO:root:      Uploaded PO-001.txt (1644191258008) 212 bytes
INFO:root:      Uploaded PO-002.txt (1644183556404) 229 bytes
INFO:root:      Uploaded PO-003.txt (1644182101485) 222 bytes
INFO:root:      Uploaded PO-004.txt (1644181292827) 217 bytes
INFO:root:      Uploaded PO-005.txt (1644196259522) 211 bytes
```
A sample document was uploaded to the Box folder `All files -> Workshops -> intelligence`. Open your Box app and check the content of the folders.



## Extract

Create a `intelligence_extract.py` file on the root of the project that you will use to write your code.

For the DEMO_FILE constant, use the file id from the previous step, in my case it is `1644174078580`.


```python
import json
import logging

from box_sdk_gen import AiResponse, CreateAiAskItems

from utils.box_ai_client_oauth import BoxAIClient, ConfigOAuth, get_ai_client_oauth

logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)

SAMPLE_INVOICE = "1644174078580"


def main():
    """Simple script to demonstrate how to use the Box SDK"""
    conf = ConfigOAuth()
    client = get_ai_client_oauth(conf)

    me = client.users.get_user_me()
    print(f"\nHello, I'm {me.name} ({me.login}) [{me.id}]")
    print("-" * 50)
    print()


if __name__ == "__main__":
    main()
```

Resulting in:

```yaml
Hello, I'm Rui Barbosa (barduinor@gmail.com) [18622116055]
```

Now, let's create a method to extract the data from the document.

```python
def intelligence_extract(client: BoxAIClient, file_id: str, prompt: str) -> AiResponse:
    items = CreateAiAskItems(id=file_id, type="file")

    ai_response: AiResponse = client.intelligence.extract(prompt=prompt, items=[items])

    return ai_response
```

Next, let's create a input prompt, and call this method on our main.

```python
def main():
    ...
    # Using a plain english prompt
    prompt = "find the document type (invoice or po), document number, date, vendor, total, and po number"
    ai_response = intelligence_extract(client, SAMPLE_INVOICE, prompt)
    print(f"Prompt: {prompt}\nResponse: \n{ai_response.answer}\n")
```

This will result in:

```yaml
Prompt: find the document type (invoice or po), document number, date, vendor, total, and po number
Response: 
{"document type": "invoice", "document number": "B1234", "date": "March 13, 2024", "vendor": "Galactic Gizmos Inc.", "total": "$575", "po number": "001"}
```

The prompt can be in a more structured format, for example:

```python
def main():
    ...
    # Using a more explicit prompt
    prompt = '{"document_type","document_number","date","vendor","total","PO"}'
    ai_response = intelligence_extract(client, SAMPLE_INVOICE, prompt)
    print(f"Prompt: {prompt}\nResponse: \n{ai_response.answer}\n")    
```

Results in:
```yaml
Prompt: {"document_type","document_number","date","vendor","total","PO"}
Response: 
{"document_type": "Invoice", "document_number": "B1234", "date": "March 13, 2024", "vendor": "Galactic Gizmos Inc.", "total": "$575", "PO": "001"}
```

The prompt can accept a JSON sting with a more structured prompt.
For example, converting a dictionary with a formal structure to a JSON string:

```python
def main():
    ...
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
    print(f"Prompt: {prompt}\nResponse: \n{ai_response.answer}")
```

Resulting in:
```yaml
Prompt: {
  "fields": [
    {
      "key": "documentType",
      "type": "string"
    },
    {
      "key": "doc_number",
      "type": "string"
    },
    {
      "key": "date",
      "type": "date"
    },
    {
      "key": "vendor",
      "type": "string"
    },
    {
      "key": "total",
      "type": "float"
    },
    {
      "key": "poNumber",
      "type": "string"
    }
  ]
}
Response: 
{"documentType": "Invoice", "doc_number": "B1234", "date": "2024-03-13", "vendor": "Galactic Gizmos Inc.", "total": 575.0, "poNumber": "001"}
```

## Extract structured

For complete control of the structure of the output, you can use the `/ai/extract_structured/` endpoint.
Let's create a method to call this endpoint.

```python
def intelligence_extract_structured(
    client: BoxAIClient,
    file_id: str,
    fields: List[ExtractStructuredField],
    metadata_template: ExtractStructuredMetadataTemplate,
) -> AiResponse:
    items = CreateAiAskItems(id=file_id, type="file")

    # file = client.files.get_file_by_id(file_id)
    ai_response: AiResponse = client.intelligence.extract_structured(
        items=[items], fields=fields, metadata_template=metadata_template
    )

    return ai_response
```

Now, let's create a method to call this endpoint.
We need to create a list of fields that we want to extract from the document.

```python
def main():
    ...

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
```

Resulting in:
```yaml
Using Extract structured
Response: 
{'date': '2024-03-13', 'doc_number': 'B1234', 'total': 575, 'documentType': 'Invoice', 'poNumber': '001', 'vendor': 'Galactic Gizmos Inc.'}
```



## Extra credit
You probably noticed that the document is always the same, and the data extracted is always the same.
* Create a loop to extract the data from all the Invoices in the folder.
* Do the same for the Purchase Orders.

You probably noticed tha `metadata_template` parameter on the `intelligence_extract_structured` method.
Checkout the metadata workshop to learn more about it.


## Final thoughts

This workshop provided a hands-on exploration of the new Box AI Extract endpoints, showcasing the potential of these tools to transform unstructured documents into structured data. The exercises guided you through setting up the environment, creating sample content, and extracting information using both the less formal `/ai/extract/` and the highly customizable `/ai/extract_structured/` endpoints.

### Key takeaways include:

* **Understanding Box AI Extract Endpoints**: We learned the differences between /ai/extract/ and /ai/extract_structured/ and how each endpoint serves different needs depending on the structure required for the extracted data.
* **Building Practical Skills**: The exercises demonstrated how to set up the Box AI client, query documents, and refine prompts to obtain precise, structured data, whether it's in plain language or a strictly defined format.
* **Using Structured Data**: By using structured prompts and predefined field types, you gain precise control over the data extraction process, allowing for seamless integration with other systems and enhancing the automation of workflows.

As Box AI continues to evolve, these skills will become increasingly valuable, especially for organizations looking to automate document processing and data extraction tasks. With the release of the official documentation and further enhancements, you can look forward to even more robust capabilities from Box AI.

This foundational knowledge sets the stage for more complex automation scenarios, making Box AI a powerful tool in your data handling toolkit.






