import sys
from pathlib import Path

from pydantic import ValidationError

# Project root must be on sys.path so `from app...` works when run as a script.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.models import (
    TaskCreate,
    TaskUpdate,
    TaskStatus,
    TaskPriority,
    CommentCreate,
    CommentUpdate,
)


def expect_fail(label, fn):
    try:
        fn()
        print(f"FAIL: {label} — value was accepted but should have been rejected")
    except ValidationError:
        print(f"PASS: {label}")


def expect_ok(label, fn):
    try:
        fn()
        print(f"PASS: {label}")
    except Exception as e:
        print(f"FAIL: {label} — {e}")


# 1. Whitespace title rejected
expect_fail(
    "whitespace title rejected",
    lambda: TaskCreate(title=" ", tags=["x"], comment="c"),
)

# 2. Empty title rejected
expect_fail(
    "empty title rejected",
    lambda: TaskCreate(title="", tags=["x"], comment="c"),
)

# 3. Title over 200 chars rejected
expect_fail(
    "title > 200 chars rejected",
    lambda: TaskCreate(title="x" * 201, tags=["x"], comment="c"),
)

# 4. Valid title accepted, defaults applied
def _ok_defaults():
    t = TaskCreate(title="Hello", tags=["general"], comment="hello note")
    assert t.status == TaskStatus.TODO
    assert t.priority == TaskPriority.MEDIUM
    assert t.description == ""
    assert t.assignee is None
    assert t.tags == ["general"]
    assert t.comment == "hello note"


expect_ok(
    "defaults applied (status=ToDo, priority=Medium, description='')",
    _ok_defaults,
)

# 5. extra='forbid' — unknown field rejected on TaskCreate
expect_fail(
    "extra field rejected on TaskCreate",
    lambda: TaskCreate(title="x", tags=["x"], comment="c", made_up="value"),
)

# 6. id NOT settable via TaskCreate
expect_fail(
    "id rejected on TaskCreate",
    lambda: TaskCreate(title="x", tags=["x"], comment="c", id="abc"),
)

# 7. created_at NOT settable via TaskUpdate
expect_fail(
    "created_at rejected on TaskUpdate",
    lambda: TaskUpdate(created_at="2025-01-01T00:00:00Z"),
)

# 7b. Explicit null title rejected on TaskUpdate (omit still allowed)
expect_fail(
    "null title rejected on TaskUpdate",
    lambda: TaskUpdate.model_validate({"title": None}),
)


def _ok_omit_title_on_update():
    u = TaskUpdate(priority=TaskPriority.LOW)
    assert "title" not in u.model_dump(exclude_unset=True)


expect_ok("omitted title allowed on TaskUpdate", _ok_omit_title_on_update)

# 8. Invalid enum value rejected
expect_fail(
    "invalid status rejected",
    lambda: TaskCreate(title="x", tags=["x"], comment="c", status="Whatever"),
)

# 9. Blank tag values are ignored (not stored)
def _ok_blank_tags_ignored():
    t = TaskCreate(title="x", tags=["valid", "  ", ""], comment="c")
    assert t.tags == ["valid"]
    empty = TaskCreate(title="x", tags=["", "   "])
    assert empty.tags == []


expect_ok("blank tag values ignored", _ok_blank_tags_ignored)

# 10. Tags trimmed and normalized (whitespace stripped, case-folded, duplicates removed)
def _ok_tags_normalized():
    t = TaskCreate(
        title="x",
        tags=[" Urgent ", "urgent", "Backend"],
        comment="c",
    )
    assert t.tags == ["urgent", "backend"]


expect_ok("tags trimmed, lowercased, and de-duplicated", _ok_tags_normalized)

# 11. Blank comment text rejected on CommentCreate
expect_fail("blank comment text rejected", lambda: CommentCreate(text="   "))

# 12. Valid comment text accepted and trimmed
def _ok_comment_text():
    c = CommentCreate(text="  Needs review  ")
    assert c.text == "Needs review"
    u = CommentUpdate(text="  Updated note  ")
    assert u.text == "Updated note"


expect_ok("comment text accepted and trimmed", _ok_comment_text)

# 13. Missing comment on TaskCreate allowed (optional)
def _ok_missing_comment():
    t = TaskCreate(title="x", tags=["x"])
    assert t.comment is None


expect_ok("missing comment allowed on TaskCreate", _ok_missing_comment)

# 14. Blank comment on TaskCreate treated as no comment (Option A)
def _ok_blank_comment():
    t = TaskCreate(title="x", tags=["x"], comment="   ")
    assert t.comment is None


expect_ok("blank comment treated as None on TaskCreate", _ok_blank_comment)

# 15. Comment on TaskCreate trimmed
def _ok_task_comment_trimmed():
    t = TaskCreate(title="x", tags=["x"], comment="  optional note  ")
    assert t.comment == "optional note"


expect_ok("task create comment trimmed", _ok_task_comment_trimmed)

# 16. Missing tags on TaskCreate default to empty list
def _ok_missing_tags():
    t = TaskCreate(title="x")
    assert t.tags == []
    assert t.comment is None


expect_ok("missing tags default to [] on TaskCreate", _ok_missing_tags)

# 17. Empty tags allowed on TaskUpdate
def _ok_empty_tags_update():
    u = TaskUpdate(tags=[])
    assert u.tags == []


expect_ok("empty tags allowed on TaskUpdate", _ok_empty_tags_update)

print("--- Part A verifications complete ---")
