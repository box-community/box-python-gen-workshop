# Sign

## Pre-requisites
Make sure your Box app is configured to use the following scopes:

![Alt text](img/sign-specific-scope.png)

> ### Note
> If the application scope is not available, then your account can not use the Sign API and you wont be able to complete this exercise.

## Concepts


## Sign API
References to our documentation:
* [SDK Sign](https://github.com/box/box-python-sdk-gen/blob/main/docs/sign_requests.md)
* [API Guide](https://developer.box.com/guides/box-sign/)
* [API Reference ](https://developer.box.com/reference/resources/sign-request/)

# Exercises
## Setup
Create a `sign_init.py` file on the root of the project and execute the following code:
```python
"""create sample content to box"""
import logging
from utils.box_client_oauth import ConfigOAuth, get_client_oauth

from workshops.sign.create_samples import create_samples

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
```
INFO:root:Folder workshops with id: 234108232105
INFO:root:Folder sign with id: 234103953351
INFO:root:Folder signed docs with id: 234102987614
INFO:root:Folder docs with id: 234103761574
INFO:root:      Uploaded Simple-PDF.pdf (1355143830404) 17509 bytes
```

Next, create a `sign.py` file on the root of the project that you will use to write your code.
Take note of the above document id's and include statics for them in the doce.

```python
"""Box Shared links"""
import logging

from utils.box_client_oauth import ConfigOAuth, get_client_oauth
from box_sdk_gen.schemas import (
    SignRequestCreateSigner,
    FileBaseTypeField,
    FolderBaseTypeField,
    FileBase,
    FolderMini,
)

logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)

SIGN_DOCS_FOLDER = "234102987614"

SIMPLE_PDF = "1355143830404"


def sign_doc_single(
    client: Client,
    doc_id: str,
    signer_email: str,
    sign_docs_folder: str,
    is_document_preparation_needed: bool = False,
) -> SignRequest:
    """Single doc sign by single signer"""
    # make sure file is accessible to this user
    file = client.files.get_file_by_id(file_id=doc_id)
    return client.sign_requests.create_sign_request(
        signers=[SignRequestCreateSigner(email=signer_email)],
        parent_folder=FolderMini(
            id=sign_docs_folder, type=FolderBaseTypeField.FOLDER.value
        ),
        source_files=[FileBase(id=file.id, type=FileBaseTypeField.FILE.value)],
        is_document_preparation_needed=is_document_preparation_needed,
    )


def main():
    """Simple script to demonstrate how to use the Box SDK"""
    conf = ConfigOAuth()
    client = get_client_oauth(conf)

    user = client.users.get_user_me()
    print(f"\nHello, I'm {user.name} ({user.login}) [{user.id}]")


if __name__ == "__main__":
    main()
```
Resulting in:
```
Hello, I'm Rui Barbosa  [18622116055]
```

## Sign a document
Create a method to sign a document with a single signer:
```python
def sign_doc_single(
    client: Client,
    doc_id: str,
    signer_email: str,
    sign_docs_folder: str,
    is_document_preparation_needed: bool = False,
) -> SignRequest:
    """Single doc sign by single signer"""
    # make sure file is accessible to this user
    file = client.files.get_file_by_id(file_id=doc_id)
    return client.sign_requests.create_sign_request(
        signers=[SignRequestCreateSigner(email=signer_email)],
        parent_folder=FolderMini(
            id=sign_docs_folder, type=FolderBaseTypeField.FOLDER.value
        ),
        source_files=[FileBase(id=file.id, type=FileBaseTypeField.FILE.value)],
        is_document_preparation_needed=is_document_preparation_needed,
    )
```
And use it in the main method. In my case I'm using a different email for the signer from the one I'm in my Box account. Use an email that you have access to:
```python
def main():
    ...

    # Simple sign request
    simple_sign_request = sign_doc_single(
        client,
        SIMPLE_PDF,
        "barbasr@gmail.com",
        SIGN_DOCS_FOLDER,
        False,
    )
    print(f"\nSimple sign request: {simple_sign_request.id}")
    print(f"  Status: {simple_sign_request.status.value}")
    print(f"  Signers: {simple_sign_request.signers[0].email}")
    print(f"  Prepare url: {simple_sign_request.prepare_url}") 
```

Resulting in:

```
Simple sign request: 97ac3486-5fe1-42e0-9ed2-3234e8e2129f
  Status: converting
  Signers: barduinor@gmail.com
  Prepare url: None
```
In the mean time check your Box Sign app and you should see something like this:
![Alt text](img/sign-request-pending.png)
Feel free to inspect the details of the sign request.

You should have also received an email with the sign request:
![Alt text](img/sign-request-email.png)

Lets sign the document. Click on the link and you should see something like this:


## Extra Credit


# Final thoughts


