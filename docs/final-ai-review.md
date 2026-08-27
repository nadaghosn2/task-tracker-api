# 1. AGENTS.md confirmation

Confirmed: `AGENTS.md` exists at the repository root and includes:

- **Stack:** Python 3.11, FastAPI, Pydantic v2, pytest, and vanilla JavaScript (`AGENTS.md`, lines 12–20).
- **Run/test commands:** Commands for starting the API, running pytest, and serving the frontend (`AGENTS.md`, lines 22–38).
- **Project rules:** Valid statuses, priorities, transitions, input validation, tag normalization, comment limits, and Module 5 scope restrictions (`AGENTS.md`, lines 40–55).
- **Docs-first/read-first guardrails:** It explicitly requires a docs-first, read-only-by-default workflow and requires inspecting supporting files before making repository claims (`AGENTS.md`, lines 57–64).

The phrase “read-first” is not used literally, but the requirement to inspect and cite files before making claims provides that guardrail.


# 2. AI code review mini-log
## 2.1 AI generated: Task Tracker code review summary

| Number ID | Claim | Evidence summary | Assumption to verify | Grade | Decision | Verification or decision |
|---:|---|---|---|---|---|---|
| 1 | The repo implements a task-management REST API with task CRUD, filters, and task-comment endpoints. | Routes cover task creation, listing, retrieval, partial update, deletion, and comments; listing accepts status, priority, and tag filters. | Endpoint behavior matches the handlers. | Useful | Retain | Run the existing API tests. |
| 2 | Task data is process-local and non-persistent. | Storage uses the module-level `_tasks` dictionary directly. | No startup code repopulates it. | Useful | Retain | Inspect startup/import paths if persistence is later added. |
| 3 | The API validates and normalizes task inputs. | Extra fields are forbidden; titles are trimmed and constrained; tags are normalized and de-duplicated. | Clients receive the intended validation-error responses. | Useful | Retain | Test invalid request payloads. |
| 4 | Workflow status changes are constrained. | Only the defined forward/backward and unchanged status pairs are allowed; PATCH invokes the validator. | The permitted transitions match product requirements. | Useful | Retain | Confirm workflow rules with the product owner. |
| 5 | A single-file browser Kanban UI consumes the API. | The frontend has three status columns and sends load/create/update/delete task requests. | Its API endpoint configuration fits the target environment. | Useful | Retain | Check frontend configuration in the intended deployment. |

## 2.2 My human grading

Task Tracker code review summary

| Number ID | Claim | Evidence summary | Assumption to verify | Grade | Decision | Verification or decision | my_grade | my_reason | my_next_steps |
|---:|---|---|---|---|---|---|---|---|---|
| 3 | The API validates and normalizes task inputs. | Extra fields are forbidden; titles are trimmed and constrained; tags are normalized and de-duplicated. | Clients receive the intended validation-error responses. | Useful | Retain | Test invalid request payloads. | Useful | Fields are well defined | Retain |
| 4 | Workflow status changes are constrained. | Only the defined forward/backward and unchanged status pairs are allowed; PATCH invokes the validator. | The permitted transitions match product requirements. | Useful | Retain | Confirm workflow rules with the product owner. | Noise | workflow is known to be constrained | Not to retain |
| 5 | A single-file browser Kanban UI consumes the API. | The frontend has three status columns and sends load/create/update/delete task requests. | Its API endpoint configuration fits the target environment. | Useful | Retain | Check frontend configuration in the intended deployment. | Useful | It reflects the screen that end user will see  | Retain |

# 3. AI security mini-review

## 3.1 AI generated
Security Review T1

| Number ID | Findings | File evidence | Grade | Reason | Next action |
|---|---|---|---|---|---|
| SEC-01 | Unbounded task fields and an unpaginated in-memory task collection can allow memory and response-size exhaustion if the API is exposed beyond local course use. | `app/models.py:108-114` defines `description`, `assignee`, `tags`, and `comment` without length or count limits; `app/models.py:134-139` limits only `title`; `app/storage.py:16` stores tasks in module-level `_tasks`; `app/storage.py:83-91` returns all matching tasks. | valid | The controls described as absent are not present in the inspected code. The impact depends on deployment exposure, but the resource-exhaustion condition is real. | Defer during Module 5; if deployment is approved, define field/tag limits and pagination before exposure. |
| SEC-02 | An explicit `PATCH` payload with `"tags": null` reaches storage re-validation, and the route returns the raw exception string in its 422 response. | `app/models.py:188-196` makes update `tags` optional; `app/models.py:261-263` returns explicit `None`; `app/storage.py:152-156` re-validates against `TaskResponse`; `app/models.py:266-278` requires `tags: List[str]`; `app/main.py:264-270` exposes `str(exc)`. | valid | The code path and raw-error response are directly visible. This is low-severity error-handling disclosure, not evidence of secret or traceback exposure. | Defer during Module 5; if a minimal app fix is approved, reject explicit null tags at request validation and return a stable 422 detail. |
| SEC-03 | CORS allows the opaque `null` origin and wildcard methods and headers. | `app/main.py:41-49` includes `"null"` in `allow_origins` and uses `allow_methods=["*"]` and `allow_headers=["*"]`; credentials are disabled. | valid | The configuration is present exactly as reported. The lack of credentials reduces impact, but it remains an unnecessary permission for non-local deployment. | Defer during Module 5; remove `null` and enumerate required methods and headers before non-local deployment. |
| SEC-04 | CI uses mutable action tags and installs dependencies without hash verification or a vulnerability scan. | `.github/workflows/ci.yml:14-32` uses `actions/checkout@v4`, `actions/setup-python@v5`, and `actions/cache@v4`, then runs `pip install -r requirements.txt`; `requirements.txt:1-7` pins direct dependencies but provides no hashes. | valid | The reported supply-chain controls are absent from the workflow and manifest. This is a hardening gap rather than evidence of a currently compromised dependency. | Defer during Module 5; before release or deployment, pin actions to reviewed SHAs, adopt hash verification, and add dependency scanning. |
| SEC-05 | The Docker image uses mutable `python:3.11-slim` tags in both build stages. | `Dockerfile:4` and `Dockerfile:23` specify `FROM python:3.11-slim`; `Dockerfile:25-43` also shows the positive non-root runtime control. | valid | The base-image references are tags rather than immutable digests. The non-root configuration does not remove base-image provenance risk. | Defer during Module 5; pin the base image to a reviewed digest as part of a documented image-maintenance process. |

## 3.2 My human grading
Security Review T2

| Number ID | Findings | File evidence | Grade | Reason | Next action | my_grade | my_reason | my_next_action |
|---|---|---|---|---|---|---|---|---|
| SEC-01 | Unbounded task fields and an unpaginated in-memory task collection can allow memory and response-size exhaustion if the API is exposed beyond local course use. | `app/models.py:108-114` defines `description`, `assignee`, `tags`, and `comment` without length or count limits; `app/models.py:134-139` limits only `title`; `app/storage.py:16` stores tasks in module-level `_tasks`; `app/storage.py:83-91` returns all matching tasks. | valid | The controls described as absent are not present in the inspected code. The impact depends on deployment exposure, but the resource-exhaustion condition is real. | Defer during Module 5; if deployment is approved, define field/tag limits and pagination before exposure. | valid | need to have harmonized table in size and manage size | set limits for the fields |
| SEC-02 | An explicit `PATCH` payload with `"tags": null` reaches storage re-validation, and the route returns the raw exception string in its 422 response. | `app/models.py:188-196` makes update `tags` optional; `app/models.py:261-263` returns explicit `None`; `app/storage.py:152-156` re-validates against `TaskResponse`; `app/models.py:266-278` requires `tags: List[str]`; `app/main.py:264-270` exposes `str(exc)`. | valid | The code path and raw-error response are directly visible. This is low-severity error-handling disclosure, not evidence of secret or traceback exposure. | Defer during Module 5; if a minimal app fix is approved, reject explicit null tags at request validation and return a stable 422 detail. | noise | "tags: null" is not used for filter | none |
| SEC-03 | CORS allows the opaque `null` origin and wildcard methods and headers. | `app/main.py:41-49` includes `"null"` in `allow_origins` and uses `allow_methods=["*"]` and `allow_headers=["*"]`; credentials are disabled. | valid | The configuration is present exactly as reported. The lack of credentials reduces impact, but it remains an unnecessary permission for non-local deployment. | Defer during Module 5; remove `null` and enumerate required methods and headers before non-local deployment. | valid | It affect credentials | need to check manually |


# 4. Manual check
Manual Check
| number_id | what_i_checked | what_i_found | why_it_matters |
|---|---|---|---|
|1| If the application supports non-latin alphabet| The arabic and chinese can be used but there will be limitation with alignement and mixed direction| to have the application used using various languages |

# 5. Rejected and corrected AI output

| number_id | what_ai_suggested | why_i_did_not_accept | what_i_did_instead |
|---|---|---|---|
| SEC-04 | CI supply-chain integrity is not fully pinned or verified: GitHub Actions use mutable version tags (`@v4`, `@v5`) rather than commit SHAs. Direct Python dependencies are version-pinned, but installation does not enforce hashes or a fully resolved transitive lock; CI has no dependency-vulnerability scan. AI Suggestion: Pin actions by commit SHA, use a hash-locked dependency artifact, and add a dependency/SCA check to CI. | I did not accept as this will not affect the workflow | I did not retain the suggestion |

# 6. Three AI rules
a. Never paste: unverified script
b. Always verify: test each step, and step by step. Try to break the test check the resutl and restore the test
c. Record AI contributions by: mentioning the AI tools used, brief summary on tasks requested, brief summary on my inspection and decision


# 7. Ownership statement
This repo was prepared by me. I have asked support from various AI tools to provide propositions on various aspects of the application: users stories, architecture, skeleton, backend, frontend, CI workflow, docking, documentation using docstrings, security review... The AI has provided suggestions. I decided what to choose and to discard. I had added manual scripts when needed (ex: business_rules). I discarded redundant stories, redundant tests. I asked to add doctrings above each function.  
