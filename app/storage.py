from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from app.models import (
    CommentCreate,
    CommentResponse,
    CommentUpdate,
    TaskCreate,
    TaskPriority,
    TaskResponse,
    TaskStatus,
    TaskUpdate,
)

_tasks: dict[str, TaskResponse] = {}


# Create and persist a new task from validated input.
def add_task(payload: TaskCreate) -> TaskResponse:
    """Create and persist a new task from validated input.

    Args:
        payload (TaskCreate): Already-validated task fields (see
            `app.models.TaskCreate`).

    Returns:
        TaskResponse: The stored task, with a generated `id` and
            `created_at`/`updated_at` both set to the current UTC
            time. If `payload.comment` is set, it is wrapped in a
            `CommentResponse` with the same timestamp.

    Raises:
        None.
    """
    now = datetime.now(timezone.utc)
    comment = (
        CommentResponse(text=payload.comment, created_at=now)
        if payload.comment is not None
        else None
    )
    task = TaskResponse(
        id=str(uuid4()),
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        tags=payload.tags,
        comment=comment,
        created_at=now,
        updated_at=now,
    )
    _tasks[task.id] = task
    return task


# Return all stored tasks, optionally filtered.
def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    tag: Optional[str] = None,
) -> list[TaskResponse]:
    """Return all stored tasks, optionally filtered.

    Args:
        status (Optional[TaskStatus]): Exact-match filter on task
            status.
        priority (Optional[TaskPriority]): Exact-match filter on task
            priority.
        tag (Optional[str]): If provided, stripped and lowercased,
            then matched for membership against each task's
            normalized `tags` list.

    Returns:
        list[TaskResponse]: Tasks satisfying all provided filters
            (AND'ed together). Order follows insertion order of the
            underlying dict.

    Raises:
        None.
    """
    results = list(_tasks.values())
    if status is not None:
        results = [task for task in results if task.status == status]
    if priority is not None:
        results = [task for task in results if task.priority == priority]
    if tag is not None:
        normalized_tag = tag.strip().lower()
        results = [task for task in results if normalized_tag in task.tags]
    return results


# Look up a single task by id.
def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    """Look up a single task by id.

    Args:
        task_id (str): The task's unique id.

    Returns:
        Optional[TaskResponse]: The task, or `None` if no task with
            that id exists.

    Raises:
        None.
    """
    return _tasks.get(task_id)


# Apply a partial update to a stored task.
def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    """Apply a partial update to a stored task.

    Args:
        task_id (str): The task's unique id.
        payload (TaskUpdate): Fields to update; only fields
            explicitly set on `payload` (per
            `model_dump(exclude_unset=True)`) are applied.

    Returns:
        Optional[TaskResponse]: The updated task, or `None` if no
            task with `task_id` exists. If `payload` has no fields
            set, the existing task is returned unchanged.

    Raises:
        ValueError: If `payload` explicitly sets `title` to `None`
            (defense in depth; `TaskUpdate`'s own validator normally
            rejects this first).
        ValueError: Also raised as `pydantic.ValidationError` (a
            `ValueError` subclass) from the final
            `TaskResponse.model_validate(...)` re-validation if the
            merged fields are otherwise invalid for `TaskResponse` —
            e.g. an explicit `tags: null` passes `TaskUpdate`
            (`tags` is `Optional`) but fails here because
            `TaskResponse.tags` is a required `List[str]`
            [VERIFIED via TestClient: PATCH with `{"tags": null}`
            returns 422].
    """
    existing = _tasks.get(task_id)
    if existing is None:
        return None

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        return existing

    # Defense in depth: title must never be cleared on update.
    if "title" in updates and updates["title"] is None:
        raise ValueError("title is required")

    updated = existing.model_copy(
        update={**updates, "updated_at": datetime.now(timezone.utc)}
    )
    updated = TaskResponse.model_validate(updated.model_dump())
    _tasks[task_id] = updated
    return updated


# Delete a task by id.
def delete_task(task_id: str) -> bool:
    """Delete a task by id.

    Args:
        task_id (str): The task's unique id.

    Returns:
        bool: `True` if a task was deleted, `False` if no task with
            `task_id` existed.

    Raises:
        None.
    """
    if task_id not in _tasks:
        return False
    del _tasks[task_id]
    return True


# Look up whether a task exists and its comment, if any.
def get_comment(task_id: str) -> tuple[bool, Optional[CommentResponse]]:
    """Look up whether a task exists and its comment, if any.

    Args:
        task_id (str): The task's unique id.

    Returns:
        tuple[bool, Optional[CommentResponse]]: `(True, comment)` if
            the task exists (`comment` may be `None`), or
            `(False, None)` if no task with `task_id` exists.

    Raises:
        None.
    """
    task = _tasks.get(task_id)
    if task is None:
        return False, None
    return True, task.comment


# Attach a comment to a task that doesn't already have one.
def add_comment(task_id: str, payload: CommentCreate) -> Optional[CommentResponse]:
    """Attach a comment to a task that doesn't already have one.

    Args:
        task_id (str): The task's unique id.
        payload (CommentCreate): The comment to add.

    Returns:
        Optional[CommentResponse]: The newly created comment, or
            `None` if no task with `task_id` exists.

    Raises:
        ValueError: If the task already has a comment (a task holds
            at most one comment).
    """
    task = _tasks.get(task_id)
    if task is None:
        return None
    if task.comment is not None:
        raise ValueError("task already has a comment")

    comment = CommentResponse(
        text=payload.text,
        created_at=datetime.now(timezone.utc),
    )
    _tasks[task_id] = task.model_copy(
        update={"comment": comment, "updated_at": datetime.now(timezone.utc)}
    )
    return comment


# Update the text of a task's existing comment.
def update_comment(task_id: str, payload: CommentUpdate) -> Optional[CommentResponse]:
    """Update the text of a task's existing comment.

    Preserves the comment's original `created_at`.

    Args:
        task_id (str): The task's unique id.
        payload (CommentUpdate): The new comment text.

    Returns:
        Optional[CommentResponse]: The updated comment, or `None` if
            no task with `task_id` exists or the task has no comment
            to update.

    Raises:
        None.
    """
    task = _tasks.get(task_id)
    if task is None or task.comment is None:
        return None

    comment = CommentResponse(
        text=payload.text,
        created_at=task.comment.created_at,
    )
    _tasks[task_id] = task.model_copy(
        update={"comment": comment, "updated_at": datetime.now(timezone.utc)}
    )
    return comment


# Replace the text of a task's existing comment.
def replace_comment(task_id: str, payload: CommentUpdate) -> Optional[CommentResponse]:
    """Replace the text of a task's existing comment.

    Preserves the comment's original `created_at`.

    [VERIFY] This function's body is currently identical to
    `update_comment` above — both fully overwrite `text` and keep the
    original `created_at`. If PUT (`replace_comment`) is meant to
    behave differently from PATCH (`update_comment`), that
    distinction is not implemented yet.

    Args:
        task_id (str): The task's unique id.
        payload (CommentUpdate): The new comment text.

    Returns:
        Optional[CommentResponse]: The updated comment, or `None` if
            no task with `task_id` exists or the task has no comment
            to replace.

    Raises:
        None.
    """
    task = _tasks.get(task_id)
    if task is None:
        return None
    if task.comment is None:
        return None

    comment = CommentResponse(
        text=payload.text,
        created_at=task.comment.created_at,
    )
    _tasks[task_id] = task.model_copy(
        update={"comment": comment, "updated_at": datetime.now(timezone.utc)}
    )
    return comment


# Remove a task's comment, if it has one.
def delete_comment(task_id: str) -> bool:
    """Remove a task's comment, if it has one.

    Args:
        task_id (str): The task's unique id.

    Returns:
        bool: `True` if a comment was deleted, `False` if no task
            with `task_id` existed or the task had no comment.

    Raises:
        None.
    """
    task = _tasks.get(task_id)
    if task is None:
        return False
    if task.comment is None:
        return False
    _tasks[task_id] = task.model_copy(
        update={"comment": None, "updated_at": datetime.now(timezone.utc)}
    )
    return True


def _reset() -> None:
    _tasks.clear()
