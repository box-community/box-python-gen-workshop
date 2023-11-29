"""Box Tasks API example"""
from datetime import datetime, timedelta, UTC
import logging
from box_sdk_gen.fetch import APIException
from box_sdk_gen.client import BoxClient as Client
from box_sdk_gen.schemas import Task, TaskAssignment

from box_sdk_gen.managers.tasks import (
    CreateTaskItemArg,
    CreateTaskItemArgTypeField,
    CreateTaskActionArg,
    CreateTaskCompletionRuleArg,
)

from box_sdk_gen.managers.task_assignments import (
    CreateTaskAssignmentTaskArg,
    CreateTaskAssignmentTaskArgTypeField,
    CreateTaskAssignmentAssignToArg,
)

# from box_sdk_gen.managers.task_assignments import (

# )

from utils.box_client_oauth import ConfigOAuth, get_client_oauth

logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)


TASKS_ROOT = "237416051727"
SAMPLE_FILE_A = "1375158910885"
SAMPLE_FILE_B = "1375072950363"


def create_task(
    client: Client,
    file_id: str,
    action: CreateTaskActionArg,
    message: str,
    due_date: datetime,
    rule: CreateTaskCompletionRuleArg,
) -> Task:
    """Create a task"""
    file = CreateTaskItemArg(id=file_id, type=CreateTaskItemArgTypeField.FILE)
    iso_date = due_date.isoformat(timespec="seconds")
    task = client.tasks.create_task(
        item=file,
        action=action,
        message=message,
        due_at=iso_date,
        completion_rule=rule,
    )
    return task


def assign_task_to_user(
    client: Client, task_id: str, user_id: str
) -> TaskAssignment:
    """assign task"""

    task = task = CreateTaskAssignmentTaskArg(
        id=task_id, type=CreateTaskAssignmentTaskArgTypeField.TASK
    )

    assign_to = CreateTaskAssignmentAssignToArg(
        id=user_id,
    )
    assignment = client.task_assignments.create_task_assignment(
        task=task, assign_to=assign_to
    )

    return assignment


def main():
    """Simple script to demonstrate how to use the Box SDK"""
    conf = ConfigOAuth()
    client = get_client_oauth(conf)

    user = client.users.get_user_me()
    print(f"\nHello, I'm {user.name} ({user.login}) [{user.id}]")

    # create a complete task
    task_a = create_task(
        client,
        SAMPLE_FILE_A,
        CreateTaskActionArg.COMPLETE,
        "Please register this new customer",
        datetime.now(UTC) + timedelta(days=7),
        CreateTaskCompletionRuleArg.ANY_ASSIGNEE,
    )
    print(f"\nCreated task {task_a.id} for file {task_a.item.id}")

    # create and assign a review task and assign it
    task_b = create_task(
        client,
        SAMPLE_FILE_B,
        CreateTaskActionArg.REVIEW,
        "Please approve or reject this proposal",
        datetime.now(UTC) + timedelta(days=7),
        CreateTaskCompletionRuleArg.ANY_ASSIGNEE,
    )
    print(f"\nCreated task {task_b.id} for file {task_b.item.id}")

    assignment = assign_task_to_user(client, task_b.id, user.id)
    print(
        f"\nCreated assignment {assignment.id} for user {assignment.assigned_to.name}"
    )


if __name__ == "__main__":
    main()
