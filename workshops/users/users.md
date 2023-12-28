# Users



## Pre-requisites
The free Box accounts do not support files requests, so you will need to have a Box Business Plan, or a full developer account to be able to use this feature.

## Concepts

Within the Box Platform API we can't create a file request directly. We can however copy and customize an existing file request.

## Users API
References to our documentation:
* []()

# Exercises
## Setup
Create a `users_init.py` file on the root of the project and execute the following code:
```python
"""create sample content to box"""
import logging
from utils.box_client_oauth import ConfigOAuth, get_client_oauth

from workshops.users.create_samples import create_samples

logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)

conf = ConfigOAuth()


def main():
    client = get_client_oauth(conf)
    create_samples(client)


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
```
Result:
```
INFO:root:Folder workshops with id: 234108232105
INFO:root:Folder users with id: 241838082529
```

Next, create a `users.py` file on the root of the project that you will use to write your code.


```python
import logging

from box_sdk_gen.client import BoxClient as Client

from utils.box_client_oauth import ConfigOAuth, get_client_oauth


logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)


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

## Create a file request template



## File request details



## Create a file request

## Update a file request


## Delete a file request

## Extra credit

# Final thoughts







