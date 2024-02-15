# Tasks
Tasks allow users to request collaborators on a document to review it or complete a piece of work. Tasks can be used by developers to create document-centric workflows.

## Concepts
A task is primarily associated with a document.

There are two types of tasks, `review` and `complete`. 

A `review` task is used to request a collaborator to review a file, where the status can be `incomplete`, `approved` or `rejected`.

A `complete` task is used to request a collaborator to complete a piece of work. It can have the status of `incomplete` or `complete`.

A task can be assigned to single or multiple users, and has a `completion_rule` that determines if the task can be completed by any user (`any_assignee`), or requires all users (`all_assignees`).

The only way to complete a task is to complete the assignments.

A task can also have a `due_at`, specifying the date and time when the task needs to be completed, and a message describing the tasks it self.

## Tasks API
References to our documentation:
* [SDK tasks](https://github.com/box/box-python-sdk-gen/blob/main/docs/tasks.md)
* [SDK task assignments](https://github.com/box/box-python-sdk-gen/blob/main/docs/task_assignments.md)
* [API Guide](https://developer.box.com/guides/tasks/)
* [API Reference](https://developer.box.com/reference/get-files-id-tasks/)
* [Support note](https://support.box.com/hc/en-us/articles/360043695954-Adding-Comments-and-Tasks)


# Exercises
## Setup
Create a `tasks_init.py` file on the root of the project and execute the following code:
```python
"""create sample content to box"""
import logging
from utils.box_client_oauth import ConfigOAuth, get_client_oauth

from workshops.tasks.create_samples import create_samples

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
INFO:root:Folder workshops with id: 223095001439
INFO:root:Folder tasks with id: 237416051727
INFO:root:      Uploaded sample_file_B.txt (1375072950363) 42 bytes
INFO:root:      Uploaded sample_file_A.txt (1375158910885) 42 bytes
```

Next, create a `tasks.py` file on the root of the project that you will use to write your code.

Create a global constant named `TASKS_ROOT` and make it equal to the id of the `tasks` folder, in my case `237416051727`

Create a global constant named `SAMPLE_FILE_A` and make it equal to the id of the `sample_file_A.txt` file, in my case `1375158910885`

Create a global constant named `SAMPLE_FILE_B` and make it equal to the id of the `sample_file_B.txt` file, in my case `1375072950363`

```python
"""Box Tasks API example"""
from datetime import datetime, timedelta, UTC
import logging
from box_sdk_gen.errors import BoxAPIError
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


TASKS_ROOT = "237416051727"
SAMPLE_FILE_A = "1375158910885"
SAMPLE_FILE_B = "1375072950363"


def main():
    """Simple script to demonstrate how to use the Box SDK"""
    conf = ConfigOAuth()
    client = get_client_oauth(conf)

    user = client.users.get_user_me()
    print(f"\nHello, I'm {user.name} ({user.login}) [{user.id}]")


if __name__ == "__main__":
    main()
```

## Create a tasks for a file
Let us start by creating a task for a file.

```python
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
```
Using it to create a task for `sample_file_A.txt`:
```python
def main():
    ...

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


if __name__ == "__main__":
    main()
```
Result:
```yaml
Hello, I'm Free Dev 001 (...@gmail.com) [25428698627]

Created task 23863153599 for file 1375158910885
```
Now if we navigate to our file and check the activity, we'll se the task created:
![Alt text](img/tasks-new.png)

Note that the task is not assigned to anyone just yet, but it is in progress, has a due date and the message we set.

## Assigning a task to a user
Let's create a method to assign a task to a user.
```python
def assign_task_to_user(
    client: Client, task_id: str, user_id: str
) -> TaskAssignment:
    """assign task"""

    task = task = CreateTaskAssignmentTask(
        id=task_id, type=CreateTaskAssignmentTaskTypeField.TASK
    )

    assign_to = CreateTaskAssignmentAssignTo(
        id=user_id,
    )
    assignment = client.task_assignments.create_task_assignment(
        task=task, assign_to=assign_to
    )

    return assignment
```
And create a new task, this time for `SAMPLE_FILE_B`, and assign it to the user:
```python
def main():
    ...

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
```
Resulting in:
```yaml
Created task 23863571592 for file 1375072950363

Created assignment 54406160867 for user Free Dev 001
```
Now if we navigate to sample_file_b.txt in our Box app:
![Alt text](img/task-new-review-assigned.png)

Notice the task is assigned to a user, and because it is a review task, you can approve or reject it.

## List tasks on a file
Let's create a method to return all tasks on a file:
```python
def get_tasks_from_file(client: Client, file_id: str) -> Tasks:
    """List tasks"""
    tasks = client.tasks.get_file_tasks(file_id=file_id)
    return tasks
```
And a method to print the tasks:
```python
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
```

Using them in in our main:
```python
dev main()
    ...

    # list tasks
    tasks_a = get_tasks_from_file(client, SAMPLE_FILE_A)
    print("\nTasks for file A:")
    print_tasks(tasks_a)

    tasks_b = get_tasks_from_file(client, SAMPLE_FILE_B)
    print("\nTasks for file B:")
    print_tasks(tasks_b)
```
Resulting in:
```yaml
Tasks for file A:
Task 23879977594 Please register this new customer
     complete done:[False]
     2023-12-07T15:49:28+00:00
     any_assignee
Assignments: 0

Tasks for file B:
Task 23879795358 Please approve or reject this proposal
     review done:[False]
     2023-12-07T15:49:29+00:00
     any_assignee
Assignments: 1
     54437394916 Free Dev 001
     state:[incomplete]
```

## Deleting a task
Let's create a method to delete a task:
```python
def delete_task(client: Client, task_id: str):
    """Delete a task"""
    try:
        client.tasks.delete_task_by_id(task_id=task_id)
    except BoxAPIError as err:
        print(f"Error deleting task {task_id}: {err}")
```
And delete all tasks from both files:
```python
def main():
    ...

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
```
Resulting in:
```yaml
Deleting tasks for file A

Tasks for file A:
No tasks

Deleting tasks for file B

Tasks for file B:
No tasks
```
>You may not be able to delete all tasks. Completed tasks cannot be deleted.

## Completing a task
We can programmatically complete a task. This is done indirectly by assignment, meaning we update the assignment, and depending on the completion rule, the task will be completed.
Let's create a method to update an assignment:
```python
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
```
Now in the main we'll create a task, assign it to the user, and update it to a complete state with a comment:

```python
def main()
    ...

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
```
Resulting in:
```yaml
Created task 23880184540 for file 1375158910885
Assigned task 23880184540 to user Free Dev 001
Updated assignment 54438381007

Tasks for file A:
Task 23880184540 Please register this new customer
     complete done:[True]
     2023-12-07T15:59:16+00:00
     any_assignee
Assignments: 1
     54438381007 Free Dev 001
     state:[completed]
     All done boss
```
>Note that since we only had one assignment, when it was completed, the task also got completed.

## Extra Credit
There is more you can do with both tasks and task assignments, like updating them, or creating a task assignment for multiple users. Both endpoints support full CRUD operations.

* If your account has multiple users, try creating a task assignment for multiple users.
* Try updating a task or task assignment.

# Final thoughts
Both the SDK and API do not provide a way to list all tasks associated to a user, although this feature exists in the Box app. The list of tasks is only per file.

There is a set of webhooks triggers associated with tasks that you can use in your app. The `TASK_ASSIGNMENT.CREATED` and the `TASK_ASSIGNMENT.UPDATED` will allow your application to react to user interactions with tasks even if within the Box app.


