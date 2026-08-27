# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Current branch: `final-project` (tracks `origin/final-project`).

## 1. Tech stack

Pinned in `requirements.txt`:
- FastAPI 0.115.0
- Pydantic 2.9.2 (v2)
- Uvicorn 0.30.6
- python-dotenv 1.0.1

Frontend: vanilla JavaScript/HTML/CSS — `frontend/index.html` is a single static file, no framework, no build step, no `package.json`.

Python 3.11 at least —

pytest for tests —

httpx for tests —

## 2. Run command

```bash
uvicorn app.main:app --reload --port 8000
```

## 3. Test command

```bash
pytest -v
```

(Tests live only under `tests/`, so this discovers the same suite as `pytest tests/ -v`.)

## 4. Architecture summary

Backend (`app/`):
- `main.py` — FastAPI app instance, CORS config, all route handlers (`/health`, `/`, `/json/version`, `/tasks` CRUD, `/tasks/{task_id}/comments`). Routes are thin: they call into `storage`/`business_rules` and translate results into HTTP responses.
- `models.py` — Pydantic models (`TaskCreate`, `TaskUpdate`, `TaskResponse`, `CommentCreate`, `CommentUpdate`, `CommentResponse`) and field-level validation (title, tags, comment).
- `storage.py` — in-memory persistence: a module-level `dict[str, TaskResponse]`. All task and comment CRUD operates directly on this dict; a task holds at most one comment.
- `business_rules.py` — **task status transition rules live here** (see §5).
- `schemas.py` — `HealthResponse`, used by the `/health` route.

Frontend:
- `frontend/index.html` — single-file board UI (To Do / In Progress / Done columns), talks to the API at `http://localhost:8000`.

Tests (`tests/`):
- `conftest.py` — adds repo root to `sys.path`, defines the `client` and `created_task` fixtures, and an autouse fixture that resets in-memory storage between tests.
- `test_tasks.py` — the pytest suite (task CRUD, tags, comments, status transitions).
- `verify_a.py` — a standalone manual verification script (not pytest — no `test_`-prefixed functions), run directly with `python tests/verify_a.py`.

Supporting docs: `docs/midcourse/` (user-stories, mini-adr, verification, reflection) — course deliverables with rationale behind some of the business rules below.

Packaging / CI (this directory is the git repository root):
- `Dockerfile` — multi-stage build (deps into a venv, then a slim runtime stage), non-root `app` user, `HEALTHCHECK` on `/health`, `CMD` runs uvicorn without `--reload`. Build context is the repo root; `docker-run.sh` builds + runs + polls `/health`.
- `.github/workflows/ci.yml` — GitHub Actions, runs on every push and pull request: set up Python 3.11 → `pip install -r requirements.txt` → `pytest -v --tb=short`. Paths are repo-root-relative (no `working-directory` override). It does not build the Docker image and does not deploy.

## 5. Business rules

Verified directly from `app/models.py` and `app/business_rules.py`:

- `TaskStatus` values: `ToDo`, `InProgress`, `Done`.
- Valid status transitions (`VALID_TRANSITIONS` in `app/business_rules.py`):
  - `ToDo → InProgress`
  - `InProgress → Done`
  - `Done → InProgress`
  - `ToDo → ToDo`, `InProgress → InProgress`, `Done → Done` (same-status "transitions" are explicitly allowed, so re-sending the current status while updating other fields doesn't fail)
  - Any other pair raises `HTTPException(422)`.
- `title` is required and non-blank (after `.strip()`) on both create and update, max 200 characters.
- `tags` are optional (default `[]`); normalized by lowercasing, stripping, dropping blanks, and de-duplicating.
- `comment` is optional; blank/omitted → `None`, otherwise stripped. A task holds at most one comment (enforced in `app/storage.py`).

## 6. UI states and CORS notes

UI states (`frontend/index.html`, `boardState` variable): `loading`, `empty`, `ready`, `error` — rendered as skeleton loading cards, an empty-state placeholder, and a dismissible error banner respectively.

CORS (`app/main.py`, `CORSMiddleware`):
- `allow_origins`: `http://localhost:5500`, `http://127.0.0.1:5500`, `http://localhost:5173`, `"null"`
- `allow_methods`: `*`
- `allow_headers`: `*`
- `allow_credentials`: `False`

If the frontend is served from a different origin/port than the ones listed, it must be added here.

## 7. Do-not rules

- Do not add authentication/authorization.
- Do not add a database or any persistence layer.
- Do not extend the existing `Dockerfile`/`.github/workflows/ci.yml` into an actual deployment or hosting pipeline (no registry pushes, no deploy jobs, no hosting config). The current Docker + CI setup is for local/dev build and test verification only.
- Do not make major UI changes.
- Do not change public response shapes without explicit approval
- Do not remove tests to make CI pass
- Do not run destructive shell commands without explicit confirmation
- Do not use always allow for abroad shell permissions

...without asking first.

@README.md
