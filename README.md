# Task Tracker API (Module 4)

A learning-project REST API for tracking tasks and their comments, built with Python, FastAPI, and Pydantic. Storage is in-memory only; the API supports full task CRUD, tag/status/priority filtering, status-transition rules, and a single comment per task. Module 4 adds a Dockerfile and CI workflow on top of the Module 1–3 application.

This is a learning project. It is **not** deployment-ready: there is no authentication/authorization, no database or persistent storage, and no production process manager or hosting configuration (see [Limitations](#project-conventions-and-current-limitations) below).


## 1.Prequesites

- Python 3.11+
- `pip` and the standard library `venv` module
- Docker (only needed for the [Run with Docker](#run-with-docker) section)


## 2. Local 

All commands below assume your working directory is `task-tracker-api/` (this directory), which is the git repository root.

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

An `.env.example` file is provided (`PORT`, `APP_ENV`). Copying it to `.env` is optional — `python-dotenv` loads it at startup, but neither variable currently changes runtime behavior (`PORT` isn't read anywhere in `app/`, and `APP_ENV` is assigned once in `app/main.py` but not used afterward).


## 3. API quick reference

| Method | Path | Description |
|---|---|---|
| GET | `/` | API metadata and links to docs/health/tasks |
| GET | `/json/version` | Name + version (answers browser/extension version probes) |
| GET | `/health` | Health check — `{"status": "ok", "timestamp": "..."}` |
| GET | `/tasks` | List tasks, optionally filtered by `status`, `priority`, and/or `tag` query params |
| POST | `/tasks` | Create a task — returns `201` |
| GET | `/tasks/{task_id}` | Get a single task by id |
| PATCH | `/tasks/{task_id}` | Partially update a task, including status transitions |
| DELETE | `/tasks/{task_id}` | Delete a task — returns `204` |
| POST | `/tasks/{task_id}/comments` | Add a comment to a task (a task holds at most one) — returns `201` |
| GET | `/tasks/{task_id}/comments` | Get a task's comment |
| PATCH | `/tasks/{task_id}/comments` | Update a task's comment text |
| PUT | `/tasks/{task_id}/comments` | Replace a task's comment text |
| DELETE | `/tasks/{task_id}/comments` | Delete a task's comment — returns `204` |

**Valid status transitions** (`PATCH /tasks/{task_id}` with a `status` field):

| From | To |
|---|---|
| `ToDo` | `InProgress` |
| `InProgress` | `Done` |
| `Done` | `InProgress` |
| any status | itself (no-op, allowed) |

Any other transition (e.g. `ToDo` → `Done` directly) returns `422`.


## 4. Project structure

```
task-tracker-api/
├── .github/
│   └── workflows/
│       └── ci.yml         # GitHub Actions: install deps + run pytest
├── app/
│   ├── main.py            # FastAPI app instance, CORS config, all route handlers
│   ├── models.py          # Pydantic request/response models and field validation
│   ├── storage.py         # In-memory persistence (module-level dict)
│   ├── business_rules.py  # Task status transition rules
│   └── schemas.py         # HealthResponse, used by GET /health
├── frontend/
│   └── index.html         # Single-file board UI (To Do / In Progress / Done), no build step
├── tests/
│   ├── conftest.py        # Shared fixtures (client, created_task) and storage-reset fixture
│   ├── test_tasks.py      # pytest suite (44 tests)
│   └── verify_a.py        # Standalone manual verification script (not pytest)
├── docs/midcourse/        # Course deliverables: user stories, mini-ADR, verification, reflection
├── Dockerfile              # Multi-stage build, non-root user, HEALTHCHECK
├── .dockerignore
├── docker-run.sh           # Build + run + healthcheck convenience script
├── requirements.txt
└── README.md
```

The repository also contains several dated markdown notes from course modules (design drafts, verification logs, CI proof checklists) that document the process behind this work but aren't part of the running application.


## 5. Project conventions and current limitations

- **Storage is in-memory only.** Data resets whenever the process restarts; there is no database and none is planned for this module (per project constraints).
- **No authentication or authorization.** Every endpoint is open.
- **CORS is restricted** to a fixed list of local dev origins (`localhost:5500`, `127.0.0.1:5500`, `localhost:5173`, and `"null"`) — see `app/main.py`. Update this list if you serve the frontend from elsewhere.
- **A task holds at most one comment**, enforced in `app/storage.py`.
- **Status transitions are restricted**: `ToDo → InProgress`, `InProgress → Done`, `Done → InProgress`, and each status to itself; any other transition returns `422` (see `app/business_rules.py`).
- **`title` is required and non-blank** (after stripping) on both create and update, max 200 characters; `tags` are normalized (lowercased, stripped, de-duplicated); `comment` is optional and normalized similarly.
- **PATCH and PUT on `/tasks/{task_id}/comments` currently behave identically** — both fully overwrite the comment's text and preserve its original timestamp. If distinct partial-vs-full-replace semantics were intended, they aren't implemented yet.
- **`pydantic-settings` is an unused dependency** — pinned in `requirements.txt` but not referenced anywhere in `app/` or `tests/`.
- **Not deployment-ready.** The Dockerfile and CI workflow added in this module support local/dev verification (build, healthcheck, automated test runs) — they do not constitute a deployment pipeline, and no hosting, database, or auth has been added.

## 6. Technical notes / decisions

No `docs/decisions/` directory exists in this repository. The closest available technical note is the mini-ADR from the course midcourse deliverables, covering the storage and tags decisions:
- [`docs/midcourse/mini-adr.md`](docs/midcourse/mini-adr.md)

Other related course documentation lives alongside it in [`docs/midcourse/`](docs/midcourse/) (user stories, verification notes, reflection).




## 7. Final Project Section

### 7.1 Branch Name
Final-project


### 7.2 Local run command
Run the app locally

```bash
uvicorn app.main:app --reload --port 8000
```

- API base: `http://localhost:8000`
- Interactive docs (Swagger UI): `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

To also run the static frontend (a single `index.html`, no build step):
```bash
cd frontend
python -m http.server 5500
```
Then open `http://localhost:5500`. (CORS is configured in `app/main.py` to allow this origin — see `app/main.py`'s `CORSMiddleware` config if you serve the frontend from elsewhere.)



### 7.3 Docker run command
Run with Docker

Build and run manually:
```bash
docker build -t task-tracker:dev .
docker run -d --name task-tracker-dev -p 8000:8000 task-tracker:dev
curl http://localhost:8000/health
```

Or use the included convenience script, which builds the image, (re)starts the container, and polls `/health` until it reports healthy:
```bash
./docker-run.sh
```

Notes on the image (`Dockerfile`):
- Multi-stage build (`builder` installs dependencies into a virtualenv; `runtime` copies only the populated venv and `app/` source — no build tools, tests, or `.git` in the final image).
- Runs as a non-root user (`app`, uid 1000), not root.
- `HEALTHCHECK` polls `/health` every 30s using Python's stdlib `urllib` (no extra HTTP client installed).
- No `--reload` in the container's `CMD` — this is a static runtime image, not a dev server.

To stop and remove the container:
```bash
docker rm -f task-tracker-dev
```


### 7.4 Test command
Run tests

```bash
pytest -v
```

This discovers the full suite under `tests/` (currently 45 tests in `tests/test_tasks.py`, covering task CRUD, tags, comments, and status transitions).

`tests/verify_a.py` is a separate, standalone manual verification script (not part of the pytest suite — it has no `test_`-prefixed functions) and is run directly:
```bash
python tests/verify_a.py
```



### 7.5 Backend baseline verification

**Command used to start the API:**
```bash
uvicorn app.main:app --port 8000
```

**Result of `GET /health`:**
```
HTTP 200
{"status":"ok","timestamp":"2026-08-25T16:00:37.555089Z"}
```



### 7.6 Frontline verification
**How to open the frontend:**
```bash
cd frontend
python -m http.server 5500
```
Then open `http://localhost:5500` in a browser (with the API running separately via `uvicorn app.main:app --reload --port 8000`, since the frontend calls `http://localhost:8000`).

**Confirmation:** Inspected `frontend/index.html` directly and confirmed the three-column Kanban board (`To Do`, `In Progress`, `Done`, each rendered via `data-status` columns) and the create/edit task flow (`New Task` button and `#task-modal` with an `Edit Task` title triggered via `openTaskModal('edit', task)`) are both still present and intact in the markup/JS — no code was changed.




### 7.7 Test baseline verification

#### 7.7.1 Command run

```bash
pytest -v
```
(run from `task-tracker-api/`)

#### 7.7.2 Result

```
45 passed in 0.78s
```

Full suite, zero failures.

#### 7.7.3 Failing tests

None. No pre-existing-vs-introduced-by-final-work distinction is needed, since nothing failed.

#### 7.7.4 Full output

```
============================= test session starts ==============================
platform linux -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0 -- /home/esu-linux/AAC/task-tracker-api/venv/bin/python3
cachedir: .pytest_cache
rootdir: /home/esu-linux/AAC/task-tracker-api
plugins: anyio-4.14.2
collecting ... collected 45 items

tests/test_tasks.py::test_create_task_valid_returns_201_with_full_body PASSED [  2%]
tests/test_tasks.py::test_create_task_missing_title_returns_422 PASSED   [  4%]
tests/test_tasks.py::test_create_task_blank_title_returns_422 PASSED     [  6%]
tests/test_tasks.py::test_create_task_without_comment_returns_201_with_null_comment PASSED [  8%]
tests/test_tasks.py::test_create_task_blank_comment_treated_as_no_comment PASSED [ 11%]
tests/test_tasks.py::test_create_task_without_tags_returns_201_with_empty_tags PASSED [ 13%]
tests/test_tasks.py::test_create_task_invalid_priority_returns_422 PASSED [ 15%]
tests/test_tasks.py::test_create_task_unknown_field_returns_422 PASSED   [ 17%]
tests/test_tasks.py::test_list_tasks_empty_returns_200_and_empty_list PASSED [ 20%]
tests/test_tasks.py::test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list PASSED [ 22%]
tests/test_tasks.py::test_list_tasks_filter_by_priority_returns_only_matches PASSED [ 24%]
tests/test_tasks.py::test_get_task_by_id_returns_task PASSED             [ 26%]
tests/test_tasks.py::test_get_task_by_id_not_found_returns_404_with_detail PASSED [ 28%]
tests/test_tasks.py::test_patch_partial_update_keeps_other_fields PASSED [ 31%]
tests/test_tasks.py::test_patch_explicit_null_title_returns_422_and_keeps_title PASSED [ 33%]
tests/test_tasks.py::test_patch_blank_title_returns_422_and_keeps_title PASSED [ 35%]
tests/test_tasks.py::test_patch_omit_title_keeps_existing_title PASSED   [ 37%]
tests/test_tasks.py::test_patch_not_found_returns_404 PASSED             [ 40%]
tests/test_tasks.py::test_patch_valid_transition_todo_to_inprogress_returns_200 PASSED [ 42%]
tests/test_tasks.py::test_patch_status_keeps_comment_unchanged PASSED    [ 44%]
tests/test_tasks.py::test_patch_invalid_transition_todo_to_done_returns_422 PASSED [ 46%]
tests/test_tasks.py::test_patch_same_status_returns_200 PASSED           [ 48%]
tests/test_tasks.py::test_delete_existing_returns_204_no_body PASSED     [ 51%]
tests/test_tasks.py::test_delete_missing_returns_404 PASSED              [ 53%]
tests/test_tasks.py::test_patch_tags_add_remove_replace_persists PASSED  [ 55%]
tests/test_tasks.py::test_patch_tags_accepts_comma_separated_string PASSED [ 57%]
tests/test_tasks.py::test_patch_tags_not_found_returns_404 PASSED        [ 60%]
tests/test_tasks.py::test_list_tasks_filter_by_tag_returns_only_matches PASSED [ 62%]
tests/test_tasks.py::test_list_tasks_filter_by_tag_no_match_returns_empty_list PASSED [ 64%]
tests/test_tasks.py::test_patch_remove_tag_when_others_remain_keeps_other_fields PASSED [ 66%]
tests/test_tasks.py::test_patch_replace_tag_keeps_other_fields PASSED    [ 68%]
tests/test_tasks.py::test_patch_remove_all_tags_returns_200 PASSED       [ 71%]
tests/test_tasks.py::test_create_task_duplicate_tags_are_deduplicated PASSED [ 73%]
tests/test_tasks.py::test_patch_adding_existing_tag_does_not_duplicate PASSED [ 75%]
tests/test_tasks.py::test_create_task_blank_tags_are_ignored PASSED      [ 77%]
tests/test_tasks.py::test_patch_blank_tags_are_ignored PASSED            [ 80%]
tests/test_tasks.py::test_create_task_only_blank_tags_becomes_empty_list PASSED [ 82%]
tests/test_tasks.py::test_get_comment_returns_comment PASSED             [ 84%]
tests/test_tasks.py::test_add_second_comment_returns_422 PASSED          [ 86%]
tests/test_tasks.py::test_patch_comment_updates_text PASSED              [ 88%]
tests/test_tasks.py::test_patch_comment_blank_text_returns_422 PASSED    [ 91%]
tests/test_tasks.py::test_patch_comment_not_found_returns_404 PASSED     [ 93%]
tests/test_tasks.py::test_add_comment_on_task_without_comment_returns_201 PASSED [ 95%]
tests/test_tasks.py::test_delete_comment_returns_204_and_clears_comment PASSED [ 97%]
tests/test_tasks.py::test_delete_comment_when_none_returns_404 PASSED    [100%]

============================== 45 passed in 0.78s ==============================
```




### 7.8 CI workflow summary

The workflow file lives at `.github/workflows/ci.yml`, relative to this directory (`task-tracker-api/`), which is the repository root. All paths in the workflow are relative to that root.

- **Triggers:** every `push` and every `pull_request` (no branch filters).
- **Job:** runs on `ubuntu-latest`; steps run from the repository root (no `working-directory` override).
- **Steps:** checkout (`actions/checkout@v4`) → set up Python 3.11 (`actions/setup-python@v5`) → cache `~/.cache/pip` (keyed on the hash of `requirements.txt`) → `pip install --upgrade pip` → `pip install -r requirements.txt` → `pytest -v --tb=short`.
- **What it does not do:** it does not build or run the Docker image, and it does not deploy anywhere — it only installs dependencies and runs the pytest suite.




### 7.9 Evidence files
Evidence files

- [`docs/release-evidence.md`](docs/release-evidence.md)
- [`docs/final-ai-review.md`](docs/final-ai-review.md)
- [`docs/ai-playbook.md`](docs/ai-playbook.md)




### 7.10 Short AI summary
The Task Tracker is a learning application built with FastAPI, Pydantic, and vanilla JavaScript. It provides a Kanban board for creating, updating, filtering, and deleting tasks across To Do, In Progress, and Done statuses. It also supports priorities, tags, controlled status transitions, and one comment per task. Data is stored in memory, so it resets whenever the API restarts. The project includes automated tests, Docker support, and a CI workflow, but it does not include authentication or persistent database storage.