"""Box Tasks API example"""

from datetime import datetime, timedelta, UTC
import logging
from box_sdk_gen import BoxAPIError
from box_sdk_gen.client import BoxClient as Client
from box_sdk_gen.schemas import Task, TaskAssignment, Tasks

from box_sdk_gen.managers.tasks import (
    CreateTaskItem,
    CreateTaskItemTypeField,
    CreateTaskAction,
    CreateTaskCompletionRule,
)

from box_sdk_gen.managers.task_assignments import (
    CreateTaskAssignmentTask,
    CreateTaskAssignmentTaskTypeField,
    CreateTaskAssignmentAssignTo,
    UpdateTaskAssignmentByIdResolutionState,
)

from utils.box_client_oauth import ConfigOAuth, get_client_oauth

logging.basicConfig(level=logging.INFO)
logging.getLogger("box_sdk_gen").setLevel(logging.CRITICAL)


TASKS_ROOT = "237424755849"
SAMPLE_FILE_A = "1375106202533"
SAMPLE_FILE_B = "1375116033188"


def create_task(
    client: Client,
    file_id: str,
    action: CreateTaskAction,
    message: str,
    due_date: datetime,
    rule: CreateTaskCompletionRule,
) -> Task:
    """Create a task"""
    file = CreateTaskItem(id=file_id, type=CreateTaskItemTypeField.FILE)
    iso_date = due_date.isoformat(timespec="seconds")
    task = client.tasks.create_task(
        item=file,
        action=action,
        message=message,
        due_at=iso_date,
        completion_rule=rule,
    )
    return task


def assign_task_to_user(client: Client, task_id: str, user_id: str) -> TaskAssignment:
    """assign task"""

    task = task = CreateTaskAssignmentTask(id=task_id, type=CreateTaskAssignmentTaskTypeField.TASK)

    assign_to = CreateTaskAssignmentAssignTo(
        id=user_id,
    )
    assignment = client.task_assignments.create_task_assignment(task=task, assign_to=assign_to)

    return assignment


def get_tasks_from_file(client: Client, file_id: str) -> Tasks:
    """List tasks"""
    tasks = client.tasks.get_file_tasks(file_id=file_id)
    return tasks


def print_tasks(tasks: Tasks):
    if tasks.total_count == 0:
        print("No tasks")
        return tasks
    for task in tasks.entries:
        print(f"Task {task.id} {task.message}")
        print(f"     {task.action.value} done:[{task.is_completed}]")
        print(f"     {task.due_at}")
        print(f"     {task.completion_rule.value}")
        print(f"Assignments: {task.task_assignment_collection.total_count}")
        for assignment in task.task_assignment_collection.entries:
            print(f"     {assignment.id} {assignment.assigned_to.name}")
            print(f"     state:[{assignment.resolution_state.value}]")
            print(f"     {assignment.message}")


def delete_task(client: Client, task_id: str):
    """Delete a task"""
    try:
        client.tasks.delete_task_by_id(task_id=task_id)
    except BoxAPIError as err:
        print(f"Error deleting task {task_id}: {err}")


def update_task_assignment(
    client: Client,
    assignment_id: str,
    message: str,
    resolution_state: UpdateTaskAssignmentByIdResolutionState,
):
    """Update a task assignment"""
    try:
        client.task_assignments.update_task_assignment_by_id(
            task_assignment_id=assignment_id,
            message=message,
            resolution_state=resolution_state,
        )
    except BoxAPIError as err:
        print(f"Error updating task assignment {assignment_id}: {err}")


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
        CreateTaskAction.COMPLETE,
        "Please register this new customer",
        datetime.now(UTC) + timedelta(days=7),
        CreateTaskCompletionRule.ANY_ASSIGNEE,
    )
    print(f"\nCreated task {task_a.id} for file {task_a.item.id}")

    # create and assign a review task
    task_b = create_task(
        client,
        SAMPLE_FILE_B,
        CreateTaskAction.REVIEW,
        "Please approve or reject this proposal",
        datetime.now(UTC) + timedelta(days=7),
        CreateTaskCompletionRule.ANY_ASSIGNEE,
    )
    print(f"\nCreated task {task_b.id} for file {task_b.item.id}")

    assignment = assign_task_to_user(client, task_b.id, user.id)
    print(
        f"\nCreated assignment {assignment.id} for user ",
        f"{assignment.assigned_to.name}",
    )

    # list tasks
    tasks_a = get_tasks_from_file(client, SAMPLE_FILE_A)
    print("\nTasks for file A:")
    print_tasks(tasks_a)

    tasks_b = get_tasks_from_file(client, SAMPLE_FILE_B)
    print("\nTasks for file B:")
    print_tasks(tasks_b)

    # delete tasks file A
    print("\nDeleting tasks for file A")
    for task_c in tasks_a.entries:
        delete_task(client, task_c.id)
    tasks_a = get_tasks_from_file(client, SAMPLE_FILE_A)
    print("\nTasks for file A:")
    print_tasks(tasks_a)

    # delete tasks file B
    print("\nDeleting tasks for file B")
    for task_b in tasks_b.entries:
        delete_task(client, task_b.id)
    tasks_b = get_tasks_from_file(client, SAMPLE_FILE_B)
    print("\nTasks for file B:")
    print_tasks(tasks_b)

    # create, assign and complete tasks
    task_c = create_task(
        client,
        SAMPLE_FILE_A,
        CreateTaskAction.COMPLETE,
        "Please register this new customer",
        datetime.now(UTC) + timedelta(days=7),
        CreateTaskCompletionRule.ANY_ASSIGNEE,
    )
    print(f"\nCreated task {task_c.id} for file {task_c.item.id}")

    assignment_c = assign_task_to_user(client, task_c.id, user.id)
    print(f"Assigned task {task_c.id} to user {assignment.assigned_to.name}")

    update_task_assignment(
        client,
        assignment_c.id,
        "All done boss",
        UpdateTaskAssignmentByIdResolutionState.COMPLETED,
    )
    print(f"Updated assignment {assignment_c.id}")

    tasks_a = get_tasks_from_file(client, SAMPLE_FILE_A)
    print("\nTasks for file A:")
    print_tasks(tasks_a)


if __name__ == "__main__":
    main()
