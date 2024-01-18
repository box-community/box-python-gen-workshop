# Watermarks

With Groups, you have the ability to add multiple users to folders and assign access permissions quickly and easily. When implemented effectively, groups streamline deployment and make long-term user management much simpler.

## Pre-requisites
The free Box accounts do not support watermarking, so you will need to have a Box paid account, or a full developer account to be able to use this feature.

## Concepts




## Groups and membership documentation
References to our documentation:
* [SDK groups manager](https://github.com/box/box-python-sdk-gen/blob/main/docs/groups.md)
* [SDK memberships manager](https://github.com/box/box-python-sdk-gen/blob/main/docs/memberships.md)
* [Guide](https://developer.box.com/guides/collaborations/groups/)
* [Group API](https://developer.box.com/reference/resources/group/)
* [Group membership API](https://developer.box.com/reference/resources/group-membership/)
* [Admin operations](https://support.box.com/hc/en-us/articles/360043694554-Creating-and-Managing-Groups)

# Exercises
## Setup
Create a `watermark_init.py` file on the root of the project and execute the following code:
```python
"""create sample content to box"""
"""create sample content to box"""
import logging
from utils.box_client_oauth import ConfigOAuth, get_client_oauth

from workshops.watermark.create_samples import create_samples

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
INFO:root:Folder watermark with id: 244791570933
INFO:root:Folder demo_folder with id: 244792729676
INFO:root:      Uploaded sample_file.txt (1418440650584) 11 bytes
```

Next, create a `watermark.py` file on the root of the project that you will use to write your code.
Create a DEMO_FOLDER constant with the id of the `demo_folder` folder you got from the previous step.
Create a DEMO_FILE constant with the id of the `sample_file.txt` file you got from the previous step.

```python
import logging

from box_sdk_gen.client import BoxClient as Client
from box_sdk_gen.fetch import APIException
from box_sdk_gen.schemas import (
    User,
    Group,
    GroupMembership,
    Collaboration,
)
from box_sdk_gen.managers.groups import (
    CreateGroupInvitabilityLevelArg,
    CreateGroupMemberViewabilityLevelArg,
)
from box_sdk_gen.managers.memberships import (
    CreateGroupMembershipUserArg,
    CreateGroupMembershipGroupArg,
    CreateGroupMembershipRoleArg,
)

from box_sdk_gen.managers.user_collaborations import (
    CreateCollaborationItemArgTypeField,
    CreateCollaborationItemArg,
    CreateCollaborationAccessibleByArg,
    CreateCollaborationRoleArg,
    CreateCollaborationAccessibleByArgTypeField,
)


from utils.box_client_oauth import ConfigOAuth, get_client_oauth


logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)

DEMO_FOLDER = "244792729676"
DEMO_FILE = "1418440650584"


def main():
    """Simple script to demonstrate how to use the Box SDK"""
    conf = ConfigOAuth()
    client = get_client_oauth(conf)

    me = client.users.get_user_me()
    print(f"\nHello, I'm {me.name} ({me.login}) [{me.id}]")


if __name__ == "__main__":
    main()
```

Resulting in:

```
Hello, I'm Rui Barbosa (barduinor@gmail.com) [18622116055]
```

## Extra credit










