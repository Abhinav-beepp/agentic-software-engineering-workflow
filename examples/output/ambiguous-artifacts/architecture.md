# Architecture

A modular FastAPI service backed by SQLAlchemy, with a deterministic agent orchestrator around the engineering lifecycle. The URL service is separated from persistence and API adapters.

## Components
- FastAPI HTTP layer
- URLService domain/application service
- SQLAlchemy repository and models
- Agent abstractions and workflow state
- DAG-based orchestrator with retries and recovery
- Deterministic validator
- Human approval gate
- Artifact/document generator

## Data Flows
- Create URL: HTTP -> URLService -> URLRepository -> SQLite/PostgreSQL-compatible persistence.
- Redirect: HTTP -> URLService -> URLRepository -> click event + redirect response.
- Engineering workflow: requirement -> analysis -> task graph -> dependent agents -> validation -> approval -> summary.