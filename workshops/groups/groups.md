# Groups

The Box API supports a variety of users, ranging from real employees logging in with their Managed User account, to applications using App Users to drive powerful automation workflows.

## Pre-requisites
The free Box accounts do not support multiple users, so you will need to have a Box paid account, or a full developer account to be able to use this feature.

## Concepts




## Groups documentation
References to our documentation:
* [Guide](https://developer.box.com/guides/collaborations/groups/)
* [Group API](https://developer.box.com/reference/resources/group/)
* [Group membership API](https://developer.box.com/reference/resources/group-membership/)

# Exercises
## Setup
Create a `groups_init.py` file on the root of the project and execute the following code:
```python
"""create sample content to box"""
import logging
from utils.box_client_oauth import ConfigOAuth, get_client_oauth

from workshops.groups.create_samples import create_samples

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
INFO:root:Folder groups with id: 244395947100
INFO:root:      Uploaded sample_file.txt (1416059157146) 11 bytes
```

Next, create a `groups.py` file on the root of the project that you will use to write your code.


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


if __name__ == "__main__":
    main()
```

Resulting in:

```
Hello, I'm Rui Barbosa (barduinor@gmail.com) [18622116055]
```

## Listing groups

## Creating a group

## Updating a group

## Group membership

## Adding a user to a group

## Updating group membership

## Sharing with groups

## Removing a user from a group

## Deleting a group

## Extra credit
* 

# Final thoughts







