Prompt-log

# 1 Selected feature: Tags/labels (required feature) ##################################

## 1.1 PROMPT lightweight architecture proposals

### 1.1.1 - Weak prompt
write 2 proposals for lightweight architecture.

### 1.1.2 - Structured prompt for light weight architecture proposals – using ChatGPT
Context:
I am adding tags/labels to a Task Tracker application with a Python/FastAPI backend and a simple web frontend.

Reviewed requirements:
<< >> 

Constraints:
-	This is a learning project, not production software.
-	The backend must use Python, FastAPI, and Pydantic for validation.
-	I want a REST API backend and a separate simple web frontend.
-	Keep the tech stack simple, well-documented, and easy to run locally.
-	No authentication or multi-tenancy.
-	Do not suggest microservices, Docker, cloud deployment, or production database setup.

Task:
Propose two different lightweight architectures:
-	Option A should be the simplest local-storage approach appropriate for a first learning project.
-	Option B may use a lightweight local database approach if it improves realism without overcomplicating the project.

For each option, provide:
1.	Tech stack and data storage choice
2.	Folder structure
3.	Data model sketch with Pydantic fields and constraints
4.	Three trade-offs compared to the other option

Output format:
Return Option A and Option B in clearly separated sections using a table. Do not choose for me.
 
### 1.1.3 - Agent output: Proposal from ChatGPT
frontend, while enforcing the tag rules in Pydantic and the API/service layer.
Option A — JSON File Local Storage
Area	Proposal
1. Tech stack & storage	Backend: Python 3.x + FastAPI + Pydantic + Uvicorn. Storage: a single local tasks.json file. Frontend: plain HTML + CSS + vanilla JavaScript using fetch() against the REST API. No ORM or database required.
Folder structure	text<br>task-tracker/<br>├── backend/<br>│ ├── app/<br>│ │ ├── main.py<br>│ │ ├── models.py<br>│ │ ├── schemas.py<br>│ │ ├── routes/<br>│ │ │ └── tasks.py<br>│ │ └── storage.py<br>│ ├── data/<br>│ │ └── tasks.json<br>│ └── requirements.txt<br>├── frontend/<br>│ ├── index.html<br>│ ├── style.css<br>│ └── app.js<br>└── README.md<br>
3. Data model sketch	python<br>from pydantic import BaseModel, Field, field_validator<br><br>class TaskCreate(BaseModel):<br> title: str = Field(min_length=1)<br> status: str<br> priority: str<br> description: str = ""<br> assignee: str = ""<br> tags: list[str] = Field(min_length=1)<br><br> @field_validator("title", "tags")<br> @classmethod<br> def validate_values(cls, value):<br> # Reject blank titles/tags and normalize whitespace.<br> return value<br>Task records can contain: id, title, status, priority, description, assignee, and tags. Tags must contain at least one non-blank value and must not contain duplicates. The same validation should be applied when editing tags.
TAG-002 behavior	Update the task's complete tag list or individual tags. Persist the updated list to tasks.json. Return 404 for a missing task.
TAG-003 behavior	GET /tasks?tag=backend returns only tasks containing that tag. A tag with no matches returns an empty list.
TAG-004 behavior	Removing a tag is allowed only when another tag remains. Attempting to remove the only tag results in 422. Replacing the only tag with another valid tag is allowed.
TAG-005 behavior	Normalize tags before saving—for example, trim whitespace and reject duplicate values. A blank tag returns 422.
Trade-offs compared with Option B
1.	Simpler: No database library, ORM, migrations, or SQL knowledge is required.
2.	Less realistic: File-based persistence does not teach database querying or relationships as well as SQLite.
3.	More limited: As the task list grows, reading and rewriting the JSON file for changes becomes less efficient than querying SQLite.
________________________________________
Option B — SQLite Local Database
Area	Proposal
1. Tech stack & storage	Backend: Python 3.x + FastAPI + Pydantic + SQLModel + Uvicorn. Storage: local SQLite database (tasks.db). Frontend: plain HTML + CSS + vanilla JavaScript. SQLite requires no separate database server and works well for a learning project.
2. Folder structure	text<br>task-tracker/<br>├── backend/<br>│ ├── app/<br>│ │ ├── main.py<br>│ │ ├── database.py<br>│ │ ├── models.py<br>│ │ ├── schemas.py<br>│ │ └── routes/<br>│ │ └── tasks.py<br>│ ├── data/<br>│ │ └── tasks.db<br>│ └── requirements.txt<br>├── frontend/<br>│ ├── index.html<br>│ ├── style.css<br>│ └── app.js<br>└── README.md<br>
3. Data model sketch	A Task table can contain id, title, status, priority, description, assignee, and tags. For this project's scope, tags can remain a single JSON/text field containing a list of strings rather than introducing a separate Tag table. Pydantic request schemas enforce the application rules:python<br>class TaskCreate(BaseModel):<br> title: str = Field(min_length=1)<br> status: str<br> priority: str<br> description: str = ""<br> assignee: str = ""<br> tags: list[str] = Field(min_length=1)<br>Validation should reject blank tag values and duplicate tags, ensuring every task has at least one valid tag.
TAG-002 behavior	Update and persist the task's tags in SQLite. A missing task returns 404.
TAG-003 behavior	Query tasks by their stored tags. For a learning project, this can initially be implemented by loading the tag list and filtering in Python rather than introducing complex SQL.
TAG-004 behavior	Before removing a tag, validate that the resulting list still contains at least one non-blank tag. Removing the only tag returns 422; replacing it with another valid tag is allowed.
TAG-005 behavior	Pydantic validation normalizes and validates the incoming tag list before it is persisted. Duplicate or blank tags return 422.
Trade-offs compared with Option A
1.	More realistic persistence: SQLite introduces useful database concepts such as tables, queries, and persistent records without requiring a database server.
2.	Slightly more setup: SQLModel and database initialization add concepts that are unnecessary for a very small first project.
3.	Better future flexibility: Filtering, sorting, and larger task collections can eventually move into database queries instead of rewriting an entire JSON file.
________________________________________
Quick comparison
	Option A: JSON	Option B: SQLite
Learning difficulty	⭐ Simplest	⭐⭐ Slightly higher
Setup	Minimal	Still lightweight
External database server	No	No
Persistence	JSON file	SQLite file
Querying	Python/file operations	Database queries
Good for first CRUD project	Excellent	Excellent
Database concepts learned	Minimal	More
Tag storage	JSON/list in file	JSON/text field in SQLite
Frontend	HTML/CSS/JS	HTML/CSS/JS
Complexity	Lowest	Low
Both options can implement TAG-002 through TAG-005 without introducing unnecessary architecture. The key validation rule should be centralized in Pydantic/service logic: every task must have at least one non-blank, non-duplicate tag, so TAG-004 cannot accidentally leave a task with an empty tag field.

### 1.1.4 - Summary and my decision
The agent proposed 2 options of architecture designs with comparison in terms of learning difficulty, setup, external database server, querying, database concepts learned, complexity… 

I selected the option A.

## 1.2 PROMPT - Revise models.py and storage.py

### 1.2.1 - Weak prompt
Update the models.py and the storage.py

### 1.2.2 - Structured prompt to revise the models.py and the storage.py using Claude
You are a senior Python backend engineer. Adapt the TWO files for a FastAPI Task Tracker REST API.

Revise the 2 files app/models.py and app/storage.py in order to add needed tag/labels for each task. I need only the codes related to tag.

Context:
-	Tags are list or normalized comma-separated field. 
-	This project currently has a working /health endpoint from Module 1.
-	This module uses in-memory storage only.
-	Optional context from Module 1 user stories:
<<  >> 

________________________________________
FILE 1 - app/models.py
________________________________________
Use Pydantic v2 syntax only.

Define these enums:
-	TaskStatus(str, Enum): TODO = "ToDo", IN_PROGRESS = "InProgress", DONE = "Done"
-	TaskPriority(str, Enum): LOW = "Low", MEDIUM = "Medium", HIGH = "High"


Define these models:

1.	TaskCreate
-	model_config = ConfigDict(extra="forbid")
-	title: str, required, 1..200 characters after strip
-	description: Optional[str] = ""
-	status: TaskStatus = TaskStatus.TODO
-	priority: TaskPriority = TaskPriority.MEDIUM
-	assignee: Optional[str] = None
-	Include a field_validator for title that strips whitespace, rejects blank titles, and rejects titles over 200 characters.


2.	TaskUpdate
-	model_config = ConfigDict(extra="forbid")
-	all editable fields optional: title, description, status, priority, assignee
-	use the same title validator behavior only when title is provided.
-	DO NOT include id, created_at, or updated_at.

3.	TaskResponse
-	model_config = ConfigDict(extra="forbid")
-	id: str
-	title: str
-	description: str
-	status: TaskStatus
-	priority: TaskPriority
-	assignee: Optional[str]
-	created_at: datetime
-	updated_at: datetime


________________________________________
FILE 2 - app/storage.py
________________________________________
Use an in-memory module-level dictionary:
_tasks: dict[str, TaskResponse] = {}


Define exactly these functions:
-	add_task(payload: TaskCreate) -> TaskResponse
-	get_all_tasks(status=None, priority=None) -> list[TaskResponse]
-	get_task_by_id(task_id: str) -> Optional[TaskResponse]
-	update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]
-	use payload.model_dump(exclude_unset=True)
-	update updated_at when a task changes
-	delete_task(task_id: str) -> bool
-	_reset() -> None
-	clears _tasks for tests only

HARD CONSTRAINTS:
-	DO NOT use SQLAlchemy, SQLModel, Alembic, a database, or an ORM.
-	DO NOT use Pydantic v1 syntax: no @validator, no class Config, no .dict().
-	DO NOT include id, created_at, or updated_at in TaskCreate or TaskUpdate.
-	DO NOT add print or logging statements.
-	DO NOT create API routes in this step.
-	DO NOT wrap the answer in long explanation.

Output only two code blocks, each preceded by: # FILE: app/models.py FILE: app/storage.py


### 1.2.3 - Agent output from Claude
Here's just the tag-related code:
app/models.py — tag-related code

from typing import List

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
            raise ValueError("tags must not contain blank values")
        if tag not in seen:
            seen.add(tag)
            normalized.append(tag)
    return normalized

In TaskCreate:
tags: List[str]

@field_validator("tags", mode="before")
@classmethod
def normalize_tags(cls, value):
    normalized = _normalize_tags(value)
    if not normalized:
        raise ValueError("tags must contain at least one tag")
    return normalized

In TaskUpdate:
tags: Optional[List[str]] = None

@field_validator("tags", mode="before")
@classmethod
def normalize_tags(cls, value):
    if value is None:
        return None
    normalized = _normalize_tags(value)
    if not normalized:
        raise ValueError("tags must contain at least one tag")
    return normalized

In TaskResponse:
tags: List[str]

app/storage.py — tag-related code
In add_task:
tags=payload.tags,
In get_all_tasks — the tag filter parameter and its logic:
def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    tag: Optional[str] = None,
) -> list[TaskResponse]:
    results = list(_tasks.values())
    if status is not None:
        results = [task for task in results if task.status == status]
    if priority is not None:
        results = [task for task in results if task.priority == priority]
    if tag is not None:
        normalized_tag = tag.strip().lower()
        results = [task for task in results if normalized_tag in task.tags]
    return results

update_task has no tag-specific code — tags flow through the same generic payload.model_dump(exclude_unset=True) merge as every other field.
Reminder: as flagged last turn, TAG-002's 404-on-missing-task and TAG-004's "can't remove the last tag" rule are route-layer concerns not covered by this model/storage code alone.

### 1.2.4 - Summary and my decision
The agent proposed the needed modifications in the py files. For the models.py, there was need to create def_normalize_tags, and to update TaskCreate, TaskUpdate, and TaskResponse. For the storage.py, there was need to update the get_all_tasks.  

I read the content and approved it.


## 1.3 - PROMPT - Revise verify_a.py

### 1.3.1 - Weak prompt
Update the verify_a.py

### 1.3.2 - Structured prompt to revise the verify_a.py – using Claude
You are a senior Python backend engineer.

Revise the file verify_a.py to add 2 tests related to validate trimmed non-empty tag values. 

Context:
-	Tags are list or normalized comma-separated field. 
-	This project currently has a working /health endpoint from Module 1.
-	This module uses in-memory storage only.
-	Optional context from Module 1 user stories:
<<  >> 

-	Models.py file 
<< >>
-	Storage.py file
<< >>
-	Verify_a.py file:
<< >>


### 1.3.3 - Agent output
9. Blank tag value rejected
expect_fail("blank tag value rejected", lambda: TaskCreate(title="x", tags=["valid", "  "]))

10. Tags trimmed and normalized (whitespace stripped, case-folded, duplicates removed)
def _ok_tags_normalized():
    t = TaskCreate(title="x", tags=[" Urgent ", "urgent", "Backend"])
    assert t.tags == ["urgent", "backend"]

expect_ok("tags trimmed, lowercased, and de-duplicated", _ok_tags_normalized)


### 1.3.4 - Summary and my decision
The agent suggested 2 additional tests: one related to rejection of blank tag, and one to tag normalization.

I read the new tests and added them to the verify_a.py


## 1.4 - PROMPT to test and debug – using VS code

### 1.4.1 - Weak prompt
Write edge cases

### 1.4.2 - Structured prompt to test and debug – using VS code
Read the selected PATCH /tasks/{id} tests in tests/test_tasks.py.

Identify edge cases that are not currently covered related to tags. List exactly 5 scenarios. Context:
-	The frontend now uses drag-and-drop and the modal form, so PATCH is hit often.
-	Relevant areas include status changes, invalid transitions, partial updates, invalid values, not-found ids, and malformed or empty update bodies.

Output format:
N. [Scenario in one sentence]
Category: [validation | business logic | not found | malformed] Expected status: [HTTP code]
Why it matters: [one sentence]

Constraints:
-	Do not write tests yet.
-	Do not repeat scenarios already covered in the selected tests.
-	Do not suggest race conditions, SQL injection, authentication, permissions, or production database behavior.
-	Keep the scenarios realistic for this learning-project FastAPI backend.

### 1.4.3 - Agent output
Reading the PATCH `/tasks/{id}` test section now to identify missing tag-related edge cases.

Searched for regex `PATCH /tasks/{id}|patch\(|patch_tasks|PATCH .*tasks|update task|tags` (`**/tests/test_tasks.py`), 54 results

Found the relevant PATCH tag tests; reading that section to identify missing edge cases.

Read [](file:///c%3A/Users/ESU-MoPH/ACC3/mid-course-project/tests/test_tasks.py#130-130), lines 130 to 310

Read [](file:///c%3A/Users/ESU-MoPH/ACC3/mid-course-project/tests/test_tasks.py#310-310), lines 310 to 312

1. PATCH with `tags: null` should return 422.  
Category: malformed Expected status: 422  
Why it matters: the frontend could accidentally send a null tag field from an empty form value, and the API must reject invalid tag shapes.

2. PATCH with `tags` as a non-string/non-array value like `123` should return 422.  
Category: malformed Expected status: 422  
Why it matters: bad client payloads or serialization bugs should not be accepted as valid tag updates.

3. PATCH with `tags` as a comma-separated string containing blank segments like `"frontend, , api"` should return 422.  
Category: validation Expected status: 422  
Why it matters: users may enter tags with extra commas or spacing, and the backend must validate the resulting tag list.

4. PATCH with `tags` array containing a non-string element such as `["backend", 123]` should return 422.  
Category: malformed Expected status: 422  
Why it matters: tag arrays with mixed types can arise from malformed JSON and should not corrupt task tag data.

5. PATCH with `tags` as an empty string `""` should return 422.  
Category: validation Expected status: 422  
Why it matters: an empty tag payload is a realistic malformed update flow from the modal and should be rejected rather than silently accepted.

### 1.4.4 - Summary and my decision
The agent suggested 5 tests. 

The tests were similar : (1) = (5), (2) = (4) and similar to the ones in test test_tasks.py. I rejected them and used the ones in test_tasks.py. 




# 2 Selected feature: task comments (required feature) ##################################

## 2.1 - PROMPT to update models.py and storage.py

### 2.1.1 - Weak prompt
Update the files models.py and storage.py


### 2.1.2 - Structured prompt to update models.py and storage.py
You are a senior Python backend engineer. Adapt the TWO files for a FastAPI Task Tracker REST API.
Revise the 2 files app/models.py and app/storage.py in order to add needed task comment for each task.
Context:
-	Support list/add/delete behavior
-	Non-blank text validation
-	Not-found handling
-	User stories:
<<  >> 
HARD CONSTRAINTS:
-	DO NOT use SQLAlchemy, SQLModel, Alembic, a database, or an ORM.
-	DO NOT use Pydantic v1 syntax: no @validator, no class Config, no .dict().
-	DO NOT include id, created_at, or updated_at in TaskCreate or TaskUpdate.
-	DO NOT add print or logging statements.
-	DO NOT create API routes in this step.
-	DO NOT wrap the answer in long explanation.
-	DO NOT change the code.  I need to check it before accepting the changes.
-	Suggest only the codes related to task comment

### 2.1.3 - Agent outputs
For  `app/models.py` — comment-only additions

def _normalize_comment_text(value: str) -> str:
    stripped = value.strip()
    if not stripped:
        raise ValueError("comment text must not be blank")
    return stripped

class CommentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        return _normalize_comment_text(value)

class CommentUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        return _normalize_comment_text(value)

class CommentResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str
    created_at: datetime

On existing `TaskResponse`, add:
    python
comment: Optional[CommentResponse] = None

---

For `app/storage.py` — comment-only additions

In `add_task`, include:

python
comment=None,

python
from app.models import CommentCreate, CommentResponse, CommentUpdate

def get_comment(task_id: str) -> tuple[bool, Optional[CommentResponse]]:
    # (False, None) => task not found
    # (True, None)  => task found, no comment
    # (True, comment) => task found with comment
    task = _tasks.get(task_id)
    if task is None:
        return False, None
    return True, task.comment

def add_comment(task_id: str, payload: CommentCreate) -> Optional[CommentResponse]:
    # None => task not found (404)
    # ValueError => second comment (422)
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

def update_comment(task_id: str, payload: CommentUpdate) -> Optional[CommentResponse]:
    # None => task not found OR no comment (404)
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

def replace_comment(task_id: str, payload: CommentUpdate) -> Optional[CommentResponse]:
    # Updates existing comment text in place (still one comment).
    # None => task not found (404)
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

def delete_comment(task_id: str) -> bool:
    # False => task not found OR no comment (404)
    task = _tasks.get(task_id)
    if task is None or task.comment is None:
        return False

    _tasks[task_id] = task.model_copy(
        update={"comment": None, "updated_at": datetime.now(timezone.utc)}
    )
    return True

No files were modified.

### 2.1.4 - Summary and my decision
The agent suggested to add functions, classes, install libraries.
I accepted them.

## 2.2 - PROMPT to to update the CRUD endpoints

### 2.2.1 - Weak prompt
Update the CRUD endpoints if needed

### 2.2.2 - Structured prompt to update the CRUD endpoints
You are a senior Python backend engineer.
Revise the CRUD endpoints and suggest code needed for task comment. 
Context:
-	Support list/add/delete behavior
-	Non-blank text validation
-	Not-found handling
-	User stories:
<<  >> 
HARD CONSTRAINTS:
-	DO NOT wrap the answer in long explanation.
-	DO NOT change the code.  I need to check it before accepting the changes.
-	Suggest only the codes related to task comment

### 2.2.3 - Agent outputs
For `app/main.py` — comment-only additions
Update imports:
python
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

Add routes:

@app.post(
    "/tasks/{task_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["comments"],
)
def create_comment(task_id: str, payload: CommentCreate) -> CommentResponse:
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

@app.get(
    "/tasks/{task_id}/comments",
    response_model=Optional[CommentResponse],
    tags=["comments"],
)
def read_comment(task_id: str) -> Optional[CommentResponse]:
    exists, comment = storage.get_comment(task_id)
    if not exists:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )
    return comment

@app.patch(
    "/tasks/{task_id}/comments",
    response_model=CommentResponse,
    tags=["comments"],
)
def patch_comment(task_id: str, payload: CommentUpdate) -> CommentResponse:
    comment = storage.update_comment(task_id, payload)
    if comment is None:
        raise HTTPException(
            status_code=404,
            detail=f"Comment for task id {task_id} not found",
        )
    return comment

@app.put(
    "/tasks/{task_id}/comments",
    response_model=CommentResponse,
    tags=["comments"],
)
def put_comment(task_id: str, payload: CommentUpdate) -> CommentResponse:
    comment = storage.replace_comment(task_id, payload)
    if comment is None:
        raise HTTPException(
            status_code=404,
            detail=f"Comment for task id {task_id} not found",
        )
    return comment

@app.delete(
    "/tasks/{task_id}/comments",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["comments"],
)
def remove_comment(task_id: str) -> None:
    deleted = storage.delete_comment(task_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Comment for task id {task_id} not found",
        )

No files were modified.

### 2.2.4 - Summary and my decision
The agents suggested to add and update functions related to the task comment.
I approved them.


## 2.3 - PROMPT to generate test based on cases

### 2.3.1 - Weak prompt
Write a test related to task comment.

### 2.3.2 - Structured prompt to generate test based on cases
Write ONE pytest test for this Task Tracker scenario:
<< >> 
Requirements:
-	Use the existing FastAPI TestClient pattern from tests/test_tasks.py.
-	Use the same fixture style as the existing tests.
-	Name the test function so it describes the scenario exactly.
-	Arrange required data through API calls, such as POST /tasks.
-	Act with one PATCH /tasks/{id} request for the scenario.
-	Assert both the HTTP status code and the relevant response body field or detail message.
-	If the scenario is invalid input, assert that the response communicates the validation or business-rule failure.
Constraints:
-	Return only the test function.
Do not add imports unless the existing file truly lacks them.
-	Do not modify app code.
-	Do not write multiple tests in one answer.


### 2.3.3 - Agent outputs
test_patch_comment_not_found_returns_404 
test_patch_status_keeps_comment_unchanged 

### 2.3.4 - Summary and my decision
The agent suggested the tests.
I approved them and asked the agent to add them into the test_tasks.py
