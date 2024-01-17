"""Box Shared links"""
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

DEMO_FOLDER = "244395947100"


def create_group(
    client: Client,
    name: str,
    provenance: str = "box_sdk_gen",
    external_sync_identifier: str = None,
    description: str = None,
) -> Group:
    """Create group"""

    invitability_level = CreateGroupInvitabilityLevelArg.ADMINS_AND_MEMBERS
    member_viewability_level = (
        CreateGroupMemberViewabilityLevelArg.ADMINS_AND_MEMBERS
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


def list_groups(client: Client) -> None:
    """List groups"""
    print("\nGroups:")
    for group in client.groups.get_groups().entries:
        print(f" - {group.name} ({group.id})")


def add_user_to_group(
    client: Client,
    user: CreateGroupMembershipUserArg,
    group: CreateGroupMembershipGroupArg,
    role: CreateGroupMembershipRoleArg,
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


def list_group_members(client: Client, group: Group) -> None:
    """List group members"""
    print(f"\nGroup members for {group.name} ({group.id}):")
    for group_membership in client.memberships.get_group_memberships(
        group.id
    ).entries:
        print(
            f" - {group_membership.user.name} as {group_membership.role.value} [{group_membership.user.id}] "
        )


def list_user_groups(client: Client, user: User) -> None:
    """List groups for user"""
    print(f"\nGroups for {user.name} ({user.id}):")
    for group_membership in client.memberships.get_user_memberships(
        user.id
    ).entries:
        print(
            f" - {group_membership.group.name} as {group_membership.role.value} [{group_membership.group.id}] "
        )


def share_folder_with_group(
    client: Client, folder_id: str, group: Group
) -> Collaboration:
    """Share folder with group"""

    try:
        collaboration = client.user_collaborations.create_collaboration(
            item=CreateCollaborationItemArg(
                type=CreateCollaborationItemArgTypeField.FOLDER, id=DEMO_FOLDER
            ),
            accessible_by=CreateCollaborationAccessibleByArg(
                CreateCollaborationAccessibleByArgTypeField.GROUP, group.id
            ),
            role=CreateCollaborationRoleArg.EDITOR,
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


def delete_group(client: Client, group: Group) -> None:
    """Delete group"""
    client.groups.delete_group_by_id(group.id)


def main():
    """Simple script to demonstrate how to use the Box SDK"""
    conf = ConfigOAuth()
    client = get_client_oauth(conf)

    me = client.users.get_user_me()
    print(f"\nHello, I'm {me.name} ({me.login}) [{me.id}]")

    # create group
    my_group = create_group(client, "My Group")
    print(f"\nCreated group {my_group.name} ({my_group.id})")

    # list groups
    list_groups(client)

    # add me to group as administrator
    group_membership = add_user_to_group(
        client,
        CreateGroupMembershipUserArg(me.id),
        CreateGroupMembershipGroupArg(my_group.id),
        CreateGroupMembershipRoleArg.ADMIN,
    )
    print(
        f"\nAdded {group_membership.user.name} ({group_membership.user.login}) "
        f"to {group_membership.group.name} ({group_membership.group.id}) "
        f"as {group_membership.role.value}"
    )

    # list group members
    list_group_members(client, my_group)

    # list groups for me
    list_user_groups(client, me)

    # share DEMO_FOLDER with group
    collaboration = share_folder_with_group(client, DEMO_FOLDER, my_group)
    print(
        f"\nShared folder <{collaboration.item.name}> ({collaboration.item.id}) "
        f"with group <{collaboration.accessible_by.name}> ({collaboration.accessible_by.id}) "
        f"as {collaboration.role.value}"
    )

    # delete group
    delete_group(client, my_group)
    print(f"\nDeleted group {my_group.name} ({my_group.id})")


if __name__ == "__main__":
    main()
