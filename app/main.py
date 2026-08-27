# Entry point for the Task Tracker API.
# Creates the FastAPI app instance and defines the /health endpoint.

import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app import storage
from app.schemas import HealthResponse
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
from typing import Optional

from app.business_rules import validate_status_transition

# Load variables from .env into the process environment (e.g. PORT, APP_ENV).
load_dotenv()

APP_ENV = os.getenv("APP_ENV", "development")

app = FastAPI(
    title="Task Tracker API",
    description="Module 1 learning project: a simple in-memory Task Tracker REST API.",
    version="0.1.0",
)

# CORS middleware - allow only the listed origins and open methods/headers per requirements
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5173",
        "null",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)


# Return basic API metadata and links to docs/health/tasks.
@app.get("/", tags=["root"])
def root() -> dict:
    """Return basic API metadata and links to docs/health/tasks.

    Args:
        None.

    Returns:
        dict: A mapping with keys `name`, `docs`, `health`, `tasks`
            (all `str`).

    Raises:
        None.

    Example:
        GET / ->
        {"name": "Task Tracker API", "docs": "/docs",
         "health": "/health", "tasks": "/tasks"}
    """
    return {
        "name": "Task Tracker API",
        "docs": "/docs",
        "health": "/health",
        "tasks": "/tasks",
    }


# Return the API name and version for browser/extension version probes.
@app.get("/json/version", tags=["root"])
def json_version() -> dict:
    """Return the API name and version for browser/extension version probes.

    Some browsers and extensions automatically request
    `/json/version`; this route exists purely to answer that probe
    cleanly instead of returning a 404.

    Args:
        None.

    Returns:
        dict: A mapping with keys `name` (str) and `version` (str).

    Raises:
        None.

    Example:
        GET /json/version -> {"name": "Task Tracker API", "version": "0.1.0"}
    """
    # Satisfies common browser/extension probes that request /json/version.
    return {
        "name": app.title,
        "version": app.version,
    }


# Health check endpoint used to confirm the API process is running.
@app.get("/health", response_model=HealthResponse, tags=["health"])
def health() -> HealthResponse:
    """Health check endpoint used to confirm the API process is running.

    Args:
        None.

    Returns:
        HealthResponse: `status` (str) is always `"ok"`; `timestamp`
            (datetime) is the current UTC time.

    Raises:
        None.

    Example:
        GET /health ->
        {"status": "ok", "timestamp": "2026-08-25T10:00:00Z"}
    """
    return HealthResponse(
        status="ok",
        timestamp=datetime.now(timezone.utc),
    )


# List tasks, optionally filtered by status, priority, and/or tag.
@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    tag: Optional[str] = None,
) -> list[TaskResponse]:
    """List tasks, optionally filtered by status, priority, and/or tag.

    Args:
        status (Optional[TaskStatus]): If provided, only tasks with
            this exact status are returned.
        priority (Optional[TaskPriority]): If provided, only tasks
            with this exact priority are returned.
        tag (Optional[str]): If provided, the value is lowercased and
            stripped, then only tasks whose normalized `tags` list
            contains it are returned.

    Returns:
        list[TaskResponse]: Tasks matching all provided filters
            (AND'ed together). Returns all tasks if no filters are
            given.

    Raises:
        None.

    Example:
        GET /tasks?status=InProgress&tag=backend
    """
    return storage.get_all_tasks(status=status, priority=priority, tag=tag)


# Create a new task.
@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> TaskResponse:
    """Create a new task.

    Args:
        payload (TaskCreate): Task fields from the request body.
            `title` is required and non-blank (validated by
            `TaskCreate`); `status` defaults to `ToDo`, `priority`
            defaults to `Medium`, `tags` default to an empty list and
            are normalized (lowercased, stripped, de-duplicated), and
            `comment` is optional.

    Returns:
        TaskResponse: The newly created task, including generated
            `id`, `created_at`, and `updated_at`.

    Raises:
        None. `payload` is validated by `TaskCreate` before this
        function runs; invalid input never reaches this code (FastAPI
        returns 422 automatically for it).

    Example:
        POST /tasks {"title": "Write docs"} -> 201 Created
    """
    return storage.add_task(payload)


# Fetch a single task by id.
@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    """Fetch a single task by id.

    Args:
        task_id (str): The task's unique id.

    Returns:
        TaskResponse: The matching task.

    Raises:
        HTTPException: 404 if no task with `task_id` exists.

    Example:
        GET /tasks/{task_id} -> 200 with the task, or 404 if not found.
    """
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )
    return task



# Partially update a task's fields, including status transitions.
@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    """Partially update a task's fields, including status transitions.

    Only fields explicitly present in `payload` are applied; omitted
    fields are left unchanged. If `payload.status` is provided, the
    transition from the task's current status is validated against
    `business_rules.VALID_TRANSITIONS` before anything is written.

    Args:
        task_id (str): The task's unique id.
        payload (TaskUpdate): Fields to update. `title`, if present,
            must be non-blank (explicit `null` is rejected).

    Returns:
        TaskResponse: The updated task.

    Raises:
        HTTPException: 404 if no task with `task_id` exists (checked
            up front when `status` is provided, otherwise surfaced
            from `storage.update_task`).
        HTTPException: 422 if the status transition is invalid
            (raised by `validate_status_transition`), or if
            `storage.update_task` raises `ValueError` — this includes
            both its own explicit-`title: null` guard and a
            `pydantic.ValidationError` (a `ValueError` subclass) from
            re-validating the merged task, e.g. an explicit
            `tags: null` [VERIFIED via TestClient: returns 422 with
            the raw pydantic error message as `detail`].

    Example:
        PATCH /tasks/{task_id} {"status": "InProgress"}
    """
    if payload.status is not None:
        existing = storage.get_task_by_id(task_id)
        if existing is None:
            raise HTTPException(
                status_code=404,
                detail=f"Task with id {task_id} not found",
            )
        validate_status_transition(existing.status, payload.status)

    try:
        updated = storage.update_task(task_id, payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    if updated is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )
    return updated


# Delete a task by id.
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: str) -> None:
    """Delete a task by id.

    Args:
        task_id (str): The task's unique id.

    Returns:
        None. Responds with 204 No Content on success.

    Raises:
        HTTPException: 404 if no task with `task_id` exists.

    Example:
        DELETE /tasks/{task_id} -> 204 No Content.
    """
    deleted = storage.delete_task(task_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )


# Add a comment to a task.
@app.post(
    "/tasks/{task_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["comments"],
)
def create_comment(task_id: str, payload: CommentCreate) -> CommentResponse:
    """Add a comment to a task.

    A task holds at most one comment; attempting to add a second
    comment is rejected.

    Args:
        task_id (str): The task's unique id.
        payload (CommentCreate): Comment fields. `text` is required
            and non-blank.

    Returns:
        CommentResponse: The newly created comment.

    Raises:
        HTTPException: 404 if no task with `task_id` exists.
        HTTPException: 422 if the task already has a comment
            (`storage.add_comment` raises `ValueError`).

    Example:
        POST /tasks/{task_id}/comments {"text": "Looks good"} -> 201 Created
    """
    try:
        comment = storage.add_comment(task_id, payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    if comment is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )
    return comment


# Fetch the comment attached to a task, if any.
@app.get(
    "/tasks/{task_id}/comments",
    response_model=CommentResponse,
    tags=["comments"],
)
def read_comment(task_id: str) -> CommentResponse:
    """Fetch the comment attached to a task, if any.

    Args:
        task_id (str): The task's unique id.

    Returns:
        CommentResponse: The task's comment.

    Raises:
        HTTPException: 404 if no task with `task_id` exists, or if
            the task exists but has no comment.

    Example:
        GET /tasks/{task_id}/comments -> 200 with the comment, or 404
        if the task or its comment doesn't exist.
    """
    exists, comment = storage.get_comment(task_id)
    if not exists:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )
    if comment is None:
        raise HTTPException(
            status_code=404,
            detail=f"Comment for task id {task_id} not found",
        )
    return comment


# Partially update a task's comment text.
@app.patch(
    "/tasks/{task_id}/comments",
    response_model=CommentResponse,
    tags=["comments"],
)
def patch_comment(task_id: str, payload: CommentUpdate) -> CommentResponse:
    """Partially update a task's comment text.

    [VERIFY] `storage.update_comment` currently replaces the entire
    `text` field (there is no sub-field to partially update), so this
    route's behavior is identical to `put_comment` below. Confirm
    this is intentional before relying on PATCH vs PUT having
    distinct semantics.

    Args:
        task_id (str): The task's unique id.
        payload (CommentUpdate): New comment `text` (required,
            non-blank).

    Returns:
        CommentResponse: The updated comment, with its original
            `created_at` preserved.

    Raises:
        HTTPException: 404 if no task with `task_id` exists, or if
            the task has no comment to update.

    Example:
        PATCH /tasks/{task_id}/comments {"text": "Updated note"} -> 200 OK
    """
    comment = storage.update_comment(task_id, payload)
    if comment is None:
        raise HTTPException(
            status_code=404,
            detail=f"Comment for task id {task_id} not found",
        )
    return comment


# Replace a task's comment text.
@app.put(
    "/tasks/{task_id}/comments",
    response_model=CommentResponse,
    tags=["comments"],
)
def put_comment(task_id: str, payload: CommentUpdate) -> CommentResponse:
    """Replace a task's comment text.

    [VERIFY] See `patch_comment` above — `storage.replace_comment`
    has the same body as `storage.update_comment`, so PUT and PATCH
    behave identically here.

    Args:
        task_id (str): The task's unique id.
        payload (CommentUpdate): New comment `text` (required,
            non-blank).

    Returns:
        CommentResponse: The updated comment, with its original
            `created_at` preserved.

    Raises:
        HTTPException: 404 if no task with `task_id` exists, or if
            the task has no comment to replace.

    Example:
        PUT /tasks/{task_id}/comments {"text": "Replaced note"} -> 200 OK
    """
    comment = storage.replace_comment(task_id, payload)
    if comment is None:
        raise HTTPException(
            status_code=404,
            detail=f"Comment for task id {task_id} not found",
        )
    return comment


# Delete a task's comment.
@app.delete(
    "/tasks/{task_id}/comments",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["comments"],
)
def remove_comment(task_id: str) -> None:
    """Delete a task's comment.

    Args:
        task_id (str): The task's unique id.

    Returns:
        None. Responds with 204 No Content on success.

    Raises:
        HTTPException: 404 if no task with `task_id` exists, or if
            the task has no comment to delete.

    Example:
        DELETE /tasks/{task_id}/comments -> 204 No Content.
    """
    if storage.get_task_by_id(task_id) is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )
    deleted = storage.delete_comment(task_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Comment for task id {task_id} not found",
        )
