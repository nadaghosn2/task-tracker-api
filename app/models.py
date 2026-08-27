from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _normalize_tags(value) -> List[str]:
    if value is None:
        raw_items = []
    elif isinstance(value, str):
        raw_items = value.split(",")
    else:
        raw_items = list(value)

    normalized: List[str] = []
    seen = set()
    for item in raw_items:
        tag = str(item).strip().lower()
        if not tag:
            continue  # blank / whitespace-only values are ignored
        if tag not in seen:
            seen.add(tag)
            normalized.append(tag)
    return normalized


def _normalize_comment_text(value: str) -> str:
    stripped = value.strip()
    if not stripped:
        raise ValueError("comment text must not be blank")
    return stripped
    


class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class CommentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str

    # Validate and normalize comment text for creation.
    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        """Validate and normalize comment text for creation.

        Args:
            value (str): Raw `text` from the request body.

        Returns:
            str: The stripped comment text.

        Raises:
            ValueError: If the stripped text is blank (surfaced as
                HTTP 422 by FastAPI/Pydantic when this model is used
                as a request body).
        """
        return _normalize_comment_text(value)


class CommentUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str

    # Validate and normalize comment text for an update.
    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        """Validate and normalize comment text for an update.

        Args:
            value (str): Raw `text` from the request body.

        Returns:
            str: The stripped comment text.

        Raises:
            ValueError: If the stripped text is blank (surfaced as
                HTTP 422 by FastAPI/Pydantic when this model is used
                as a request body).
        """
        return _normalize_comment_text(value)


class CommentResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str
    created_at: datetime


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    description: Optional[str] = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    comment: Optional[str] = None

    # Validate and normalize a task title for creation.
    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        """Validate and normalize a task title for creation.

        Args:
            value (str): Raw `title` from the request body.

        Returns:
            str: The stripped title.

        Raises:
            ValueError: If the stripped title is blank, or exceeds
                200 characters (surfaced as HTTP 422 by
                FastAPI/Pydantic when this model is used as a request
                body).
        """
        stripped = value.strip()
        if not stripped:
            raise ValueError("title must not be blank")
        if len(stripped) > 200:
            raise ValueError("title must be at most 200 characters")
        return stripped

    # Normalize the tags field for creation.
    @field_validator("tags", mode="before")
    @classmethod
    def normalize_tags(cls, value):
        """Normalize the `tags` field for creation.

        Args:
            value: Raw tags input — `None`, a comma-separated `str`,
                or an iterable of values.

        Returns:
            List[str]: Tags lowercased, stripped, with blanks dropped
                and duplicates removed (see `_normalize_tags`).

        Raises:
            None.
        """
        return _normalize_tags(value)

    # Normalize the optional comment field for creation.
    @field_validator("comment", mode="before")
    @classmethod
    def validate_comment(cls, value):
        """Normalize the optional `comment` field for creation.

        Args:
            value: Raw comment input of any type. `None`, or a blank
                / whitespace-only string, means "no comment".

        Returns:
            Optional[str]: `None` if `value` is `None` or a blank
                string; otherwise the stripped string form of
                `value`.

        Raises:
            None. `_normalize_comment_text` is only reached once
                `value` is already known to be non-blank, so its
                blank-input `ValueError` is not reachable here.
        """
        # Option A: omit / null / blank / whitespace => no comment
        if value is None:
            return None
        if isinstance(value, str) and not value.strip():
            return None
        return _normalize_comment_text(str(value))


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    tags: Optional[List[str]] = None

    # Validate and normalize title when explicitly provided in an update.
    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, value):
        """Validate and normalize `title` when explicitly provided in an update.

        Only runs when `title` is present in the request body; an
        omitted `title` uses the field default (`None`) without
        triggering this validator, leaving the existing title
        unchanged.

        Args:
            value: Raw `title` value from the request body (only
                invoked when explicitly provided).

        Returns:
            str: The stripped title.

        Raises:
            ValueError: If `value` is explicitly `None`, the stripped
                title is blank, or it exceeds 200 characters
                (surfaced as HTTP 422 by FastAPI/Pydantic when this
                model is used as a request body).
        """
        # Option A: omit title => no change; explicit null => rejected.
        # Omitted fields use the default without running this validator.
        if value is None:
            raise ValueError("title is required")
        stripped = str(value).strip()
        if not stripped:
            raise ValueError("title must not be blank")
        if len(stripped) > 200:
            raise ValueError("title must be at most 200 characters")
        return stripped

    # Normalize the tags field when explicitly provided in an update.
    @field_validator("tags", mode="before")
    @classmethod
    def normalize_tags(cls, value):
        """Normalize the `tags` field when explicitly provided in an update.

        Args:
            value: Raw tags input, or `None` to pass `None` through
                unchanged (only invoked when `tags` is explicitly
                provided; an omitted `tags` uses the field default
                without running this validator).

        Returns:
            Optional[List[str]]: `None` if `value` is `None`;
                otherwise tags lowercased, stripped, with blanks
                dropped and duplicates removed (see
                `_normalize_tags`).

        Raises:
            None. [VERIFY] Passing an explicit `tags: null` here
            returns `None` successfully, but `storage.update_task`
            later fails to re-validate the merged task against
            `TaskResponse` (whose `tags` field is a required
            `List[str]`, not `Optional`) — confirmed via TestClient:
            `PATCH /tasks/{id}` with `{"tags": null}` returns 422
            with a raw pydantic error message. This validator itself
            does not raise; the failure happens downstream.
        """
        if value is None:
            return None
        return _normalize_tags(value)


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str]
    tags: List[str]
    comment: Optional[CommentResponse] = None
    created_at: datetime
    updated_at: datetime
