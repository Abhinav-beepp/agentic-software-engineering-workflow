# Architecture Overview

## Components

1. **Requirement Agent** normalizes intent, ambiguity, assumptions, and acceptance criteria.
2. **Planner Agent** builds a task graph with explicit dependencies and validation criteria.
3. **Architecture Agent** creates component, data-flow, decision, and trade-off information.
4. **API Contract Agent** defines the service contract.
5. **Database Agent** defines persistence structures.
6. **Implementation Bundle** produces engineering artifacts and test planning metadata.
7. **Risk Agent** records risks and mitigations.
8. **Deterministic Validator** checks required state and artifacts.
9. **Approval Gate** requires a human decision before finalization.
10. **Summary Agent** emits the final engineering outcome.

## Execution model

The orchestrator evaluates the DAG repeatedly. Tasks whose dependencies are complete become runnable. A batch of independent ready tasks executes concurrently with `asyncio.gather`, demonstrating orchestration beyond a fixed linear chain.

A failed task moves to `RETRYING` while its retry budget remains. Exhaustion moves it to `FAILED`; dependent tasks cannot proceed and become blocked.

## Control boundary

The model/provider boundary is intentionally narrow. The workflow owns state, dependencies, safety, validation, and approval. The provider may assist with reasoning/generation, but deterministic validators own checks that can be tested reliably.

## Scaling path

The demo uses SQLite. The repository layer isolates persistence so PostgreSQL can replace SQLite without changing API semantics. At higher scale, a distributed cache, stateless API replicas, asynchronous analytics pipeline, and stronger observability would be appropriate.
