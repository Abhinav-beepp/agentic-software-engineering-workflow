# Submission Checklist

The following checklist is intentionally kept in the repository so the evaluator can see how the submission maps to the assignment.

- [x] `README.md` explains approach, setup, demo, tests, assumptions, trade-offs and limitations.
- [x] Mandatory URL-shortener requirement is demonstrated.
- [x] Agent workflow is multi-step and dependency-aware.
- [x] Independent tasks can run concurrently.
- [x] Retry/recovery state is implemented.
- [x] Brownfield scanner is present and evidence-based.
- [x] Greenfield, brownfield and ambiguous examples are included with captured outputs.
- [x] API contract, database schema, generated code and generated tests are produced by the workflow.
- [x] Unit, integration, orchestration and E2E tests exist.
- [x] Deterministic validation exists.
- [x] Human approval gate exists.
- [x] Rejection/needs-revision can route the workflow back through planning and execution.
- [x] No secrets are committed.
- [x] `pytest -q` passes in the prepared environment.
- [x] Python source and generated artifacts compile successfully.
- [x] Mandatory, brownfield and ambiguous demos were executed successfully with validation passing.
- [ ] `ruff check src tests` — run in the evaluator environment if Ruff is installed.
- [ ] `mypy src` — run in the evaluator environment if mypy is installed.

## Environment note

The build/test environment used to prepare this submission had no outbound package-network access and did not have the optional Ruff/mypy executables installed. The project configuration includes both tools and their commands; this limitation does not affect the runnable application or the executed pytest suite.
