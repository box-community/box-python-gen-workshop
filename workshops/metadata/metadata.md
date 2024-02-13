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
INFO:root:Folder workshops with id: 234108232105
INFO:root:Folder metadata with id: 248842871060
INFO:root:Folder invoices with id: 248844558038
INFO:root: Folder invoices
INFO:root:      Uploaded Invoice-Q8888.txt (1443423592689) 158 bytes
INFO:root:      Uploaded Invoice-B1234.txt (1443423659957) 162 bytes
INFO:root:      Uploaded Invoice-C9876.txt (1443421455669) 183 bytes
INFO:root:      Uploaded Invoice-A5555.txt (1443416243073) 170 bytes
INFO:root:      Uploaded Invoice-Q2468.txt (1443424196411) 170 bytes
INFO:root:      Uploaded Invoice-W9999.txt (1443421799125) 173 bytes
INFO:root:      Uploaded Invoice-N7777.txt (1443427057809) 182 bytes
INFO:root:      Uploaded Invoice-N3333.txt (1443418170426) 147 bytes
INFO:root:      Uploaded Invoice-C1111.txt (1443426565707) 156 bytes
INFO:root:      Uploaded Invoice-A2222.txt (1443415638615) 160 bytes
INFO:root:Folder purchase_orders with id: 248842775394
INFO:root: Folder purchase_orders
INFO:root:      Uploaded PO-008.txt (1443424667026) 202 bytes
INFO:root:      Uploaded PO-009.txt (1443421688561) 183 bytes
INFO:root:      Uploaded PO-001.txt (1443426883092) 195 bytes
INFO:root:      Uploaded PO-002.txt (1443426820418) 212 bytes
INFO:root:      Uploaded PO-003.txt (1443416536619) 205 bytes
INFO:root:      Uploaded PO-007.txt (1443417728460) 193 bytes
INFO:root:      Uploaded PO-006.txt (1443427096385) 216 bytes
INFO:root:      Uploaded PO-010.txt (1443417666051) 188 bytes
INFO:root:      Uploaded PO-004.txt (1443422522227) 200 bytes
INFO:root:      Uploaded PO-005.txt (1443419087950) 194 bytes
```

Next, create a `metadata.py` file on the root of the project that you will use to write your code.

```python

```

Resulting in:

```yaml
Hello, I'm Rui Barbosa (barduinor@gmail.com) [18622116055]
```

## Create a metadata template

## Applying the template to the folders

## Scanning the content using the metadata suggestions

## Updating the content metadata

## Finding unmatched invoices

## Extra credit
* 

## Final thoughts









