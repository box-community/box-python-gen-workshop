"""Workshop: Watermark"""
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
