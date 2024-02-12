# Intelligence (Box AI)



## Pre-requisites


## Concepts





## Box AI documentation
References to our documentation:
* 

# Exercises
## Setup
Create a `intelligence_init.py` file on the root of the project and execute the following code:
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
INFO:root:Folder workshops with id: 234108232105
INFO:root:Folder intelligence with id: 248676986369
INFO:root:      Uploaded Box-Dive-Waiver.docx (1442379637774) 7409 bytes
```

Next, create a `intelligence.py` file on the root of the project that you will use to write your code.


```python
import logging

from utils.box_ai_client import BoxAIClient as Client

from box_sdk_gen.fetch import APIException

from utils.ai_schemas import (
    IntelligenceResponse,
    IntelligenceMode,
    IntelligenceDialogueHistory,
)


from utils.box_ai_client_oauth import ConfigOAuth, get_ai_client_oauth


logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)

DEMO_FILE = "1442379637774"


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
## Creating a group
Let's start by creating a group.
Consider this method:
```python
def create_group(
    client: Client,
    name: str,
    provenance: str = "box_sdk_gen",
    external_sync_identifier: str = None,
    description: str = None,
) -> Group:
    """Create group"""

    invitability_level = CreateGroupInvitabilityLevel.ADMINS_AND_MEMBERS
    member_viewability_level = (
        CreateGroupMemberViewabilityLevel.ADMINS_AND_MEMBERS
    )

    try:
        group = client.groups.create_group(
            name,
            provenance,
            external_sync_identifier,
            description,
            invitability_level,
            member_viewability_level,
        )
    except APIException as err:
        if err.status == 409 and err.code == "conflict":
            # group already exists
            groups = client.groups.get_groups(filter_term=name)
            for group in groups.entries:
                if group.name == name:
                    return group
    return group
```

Using this method, we can create a group with the following code:
```python
def main():
    ...

    # create group
    my_group = create_group(client, "My Group")
    print(f"Created group {my_group.name} ({my_group.id})")
``` 

Resulting in:
```yaml
Hello, I'm Rui Barbosa (barduinor@gmail.com) [18622116055]
Created group My Group (18394127658)
```

## Listing groups
Now that we have a group, we are going to need a method to list all groups.
Consider this method:
```python
def list_groups(client: Client) -> None:
    """List groups"""
    print("\nGroups:")
    for group in client.groups.get_groups().entries:
        print(f" - {group.name} ({group.id})")

def main():
    ...

    # list groups
    list_groups(client)
```

Results in:
```yaml
Groups:
 - My Group (18394127658)
```
## Adding a user to a group
A group wouldn't be very useful if we couldn't add users to it. Let's create a method to add a user to a group:
```python
def add_user_to_group(
    client: Client,
    user: CreateGroupMembershipUser,
    group: CreateGroupMembershipGroup,
    role: CreateGroupMembershipRole,
) -> GroupMembership:
    """Add user to group"""

    try:
        group_membership = client.memberships.create_group_membership(
            user, group, role
        )
    except APIException as err:
        if err.status == 409 and err.code == "conflict":
            # user already in group
            group_memberships = client.memberships.get_group_memberships(
                group.id
            )
            for group_membership in group_memberships.entries:
                if group_membership.user.id == user.id:
                    return group_membership

    return group_membership
```

Using this method, we can add a user to a group with the following code:
```python
def main():
    ...

    # add me to group as administrator
    group_membership = add_user_to_group(
        client,
        CreateGroupMembershipUser(me.id),
        CreateGroupMembershipGroup(my_group.id),
        CreateGroupMembershipRole.ADMIN,
    )
    print(
        f"\nAdded {group_membership.user.name} ",
        f"({group_membership.user.login}) ",
        f"to {group_membership.group.name} ({group_membership.group.id}) "
        f"as {group_membership.role.value}",
    )
```

Resulting in:
```yaml
Added Rui Barbosa (barduinor@gmail.com) to My Group (18394127658) as admin
```

## Listing group members
Now let's create a method to list all members of a group:
```python
def list_group_members(client: Client, group: Group) -> None:
    """List group members"""
    print(f"\nGroup members for {group.name} ({group.id}):")
    for group_membership in client.memberships.get_group_memberships(
        group.id
    ).entries:
        print(
            f" - {group_membership.user.name} as ",
            f"{group_membership.role.value} ",
            f"[{group_membership.user.id}] ",
        )
```

Using it in the main method:
```python
def main():
    ...

    # list group members
    list_group_members(client, my_group)
```

Results in:
```yaml
Group members for My Group (18394127658):
 - Rui Barbosa as admin [18622116055] 
```

## Listing user groups
We can also list all groups a user is a member of:
```python
def list_user_groups(client: Client, user: User) -> None:
    """List groups for user"""
    print(f"\nGroups for {user.name} ({user.id}):")
    for group_membership in client.memberships.get_user_memberships(
        user.id
    ).entries:
        print(
            f" - {group_membership.group.name} as ",
            f"{group_membership.role.value} ",
            f"[{group_membership.group.id}] ",
        )
```

Using it in the main method:
```python
def main():
    ...

    # list groups for me
    list_user_groups(client, me)
```

Results in:
```yaml
Groups for Rui Barbosa (18622116055):
 - My Group as admin [18394127658] 
```

## Sharing a folder with a group
Now that we understand the mechanics of groups and memberships, let's put it to use by sharing a folder with a group.
Consider this method:
```python
def share_folder_with_group(
    client: Client, folder_id: str, group: Group
) -> Collaboration:
    """Share folder with group"""

    try:
        collaboration = client.user_collaborations.create_collaboration(
            item=CreateCollaborationItem(
                type=CreateCollaborationItemTypeField.FOLDER, id=DEMO_FOLDER
            ),
            accessible_by=CreateCollaborationAccessibleBy(
                CreateCollaborationAccessibleByTypeField.GROUP, group.id
            ),
            role=CreateCollaborationRole.EDITOR,
        )
    except APIException as err:
        if err.status == 409 and err.code == "conflict":
            # folder already shared with group
            collaborations = (
                client.list_collaborations.get_folder_collaborations(folder_id)
            )
            for collaboration in collaborations.entries:
                if collaboration.accessible_by.id == group.id:
                    return collaboration

    return collaboration
```
Using this method, we can share a folder with a group with the following code:
```python
def main():
    ...

    # share DEMO_FOLDER with group
    collaboration = share_folder_with_group(client, DEMO_FOLDER, my_group)
    print(
        f"\nShared folder <{collaboration.item.name}> ",
        f"({collaboration.item.id}) ",
        f"with group <{collaboration.accessible_by.name}> ",
        f"({collaboration.accessible_by.id}) "
        f"as {collaboration.role.value}",
    )
```

Resulting in:
```yaml
Shared folder <groups> (244395947100) with group <My Group> (18394127658) as editor
```

Navigating in the box.com app to the workshops folder, we can see that the groups folder is now shared since it shows up in blue. 

![Groups folder shared](img/groups-folder.png)

We can inspect the collaboration to see that it is shared with `My Group` that we created, by clicking on the `manage collaborators` in the sub menu:

![Groups folder collaborator](img/groups-folder-collaborators.png)

## Deleting a group
Finally, let's create a method to delete a group:
```python
def delete_group(client: Client, group: Group) -> None:
    """Delete group"""
    client.groups.delete_group_by_id(group.id)
```

Using it in the main method:
```python
def main():
    ...

    # delete group
    delete_group(client, my_group)
    print(f"\nDeleted group {my_group.name} ({my_group.id})")
```

Results in:
```yaml
Deleted group My Group (18394127658)
```

## Extra credit
There are more operations available in the SDK, try implementing these:
* Update a group name and description
* Update a group membership role
* Remove a user from a group









