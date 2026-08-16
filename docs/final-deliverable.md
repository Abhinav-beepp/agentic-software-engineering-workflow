# Final Deliverable Guide

This document maps the repository to the recruiter note and assignment deliverables.

## Runnable application

The repository contains a real FastAPI URL shortener in `src/app/` with:

- URL creation
- persistent URL mappings
- short-code redirects
- click analytics
- health endpoint
- validation and structured errors
- automatic OpenAPI documentation

Run it with:

```bash
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Then visit `http://127.0.0.1:8000/docs`.

## Candidate approach

The candidate approach is documented in:

- `README.md`
- `docs/architecture.md`
- `docs/agent-workflow.md`
- `docs/design-decisions.md`

The solution uses a dependency-aware workflow rather than a generic chatbot response.

## Key decisions

- FastAPI for a small typed HTTP service and automatic OpenAPI.
- SQLAlchemy repository boundary for persistence portability.
- SQLite for zero-friction local demonstration.
- DAG orchestration to model real engineering dependencies.
- Deterministic validation for checks that should not depend on LLM variability.
- Provider abstraction with deterministic mode for reproducibility.
- Human approval before final engineering summary.

## Implementation details

The URL-shortener implementation is separated into API, service and persistence layers. The agent system has explicit state, task dependencies, retries, validation and approval transitions.

## Setup instructions

See `README.md` for exact local, Docker, demo and test commands.

## Assumptions and trade-offs

See:

- `docs/assumptions.md`
- `docs/risks-and-tradeoffs.md`
- `docs/design-decisions.md`

## Scope decision

This is intentionally a **runnable, demoable prototype**, not a production-grade distributed platform. The repository documents the path from the prototype to PostgreSQL, caching, rate limiting, authentication, asynchronous analytics, observability and stronger isolation if the system were evolved for production.
