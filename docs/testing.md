# Testing Approach

## Unit

The URL service is tested for valid creation, redirect resolution, click recording, and invalid URL rejection.

## Integration

FastAPI tests exercise creation, redirect behavior, analytics, health, persistence, and 404/422 error paths.

## Orchestration

Tests cover end-to-end workflow completion, the human approval pause, explicit rejection state, and brownfield scanning.

## Validation

The deterministic validator checks mandatory task coverage, analysis acceptance criteria, architecture presence, generated artifacts, API contract, test plan, and application entrypoint.

## Commands

```bash
pytest -q
ruff check src tests
mypy src
```
