# Task Tracker – Codex Instructions

## Project summary

This repository (root: `task-tracker-api/`) contains a learning-project Task Tracker API and a single-file browser frontend.

- Backend: FastAPI REST API for tasks and one comment per task.
- Storage: in-memory dictionary only; data resets when the API process restarts.
- Frontend: vanilla JavaScript Kanban board with To Do, In Progress, and Done columns.
- Source-of-truth implementation files: `app/main.py`, `app/models.py`, `app/storage.py`, and `app/business_rules.py`.

## Stack

- Python 3.11
- FastAPI
- Pydantic v2
- pytest
- Vanilla JavaScript frontend

See `requirements.txt` for pinned Python dependencies.

## Run and test commands

Run these from the repository root:

```bash
uvicorn app.main:app --reload --port 8000
pytest -v
```

The static frontend can be served with:

```bash
cd frontend
python -m http.server 5500
```

Docker is supported by `Dockerfile`; see `README.md` for the documented build and run commands.

CI runs on every push and pull request via `.github/workflows/ci.yml` (repo root): it sets up Python 3.11, installs `requirements.txt`, and runs `pytest -v --tb=short`. It does not build the Docker image or deploy.

## Business rules

- Valid task statuses are `ToDo`, `InProgress`, and `Done`.
- Valid priorities are `Low`, `Medium`, and `High`.
- Allowed status transitions are:
  - `ToDo` → `InProgress`
  - `InProgress` → `Done`
  - `Done` → `InProgress`
  - A status may remain unchanged.
- A task title is required, trimmed, non-blank, and at most 200 characters.
- Unknown request fields are rejected by the Pydantic request models.
- Tags are trimmed, lowercased, de-duplicated, and blank tag values are ignored.
- A task can have at most one comment. Comment text must be non-blank after trimming.
- Preserve existing API response shapes unless explicitly asked to change them.
- The API uses in-memory storage; do not add a database in Module 5.
- Do not add authentication or authorization in Module 5.

## Module 5 guardrails

- Use a docs-first and read-only-by-default workflow.
- Treat each Codex thread as one bounded task.
- Do not edit `app/` unless the user explicitly approves one specific minimal fix.
- Prefer edits under `docs/` unless the user explicitly authorizes another path.
- Before making repository claims, inspect and cite the files that support them.
- If a file or behavior is not visible, mark it as not confirmed rather than guessing.

## Security and governance

- Never paste, print, commit, or expose secrets, tokens, credentials, or `.env` contents.
- Do not run destructive commands or overwrite/delete files unless the user has explicitly authorized the exact target.
- Keep unrelated working-tree changes intact.
- Do not invent test results, runtime behavior, findings, or file contents.
- Report evidence with exact repository paths and distinguish verified facts from assumptions.
