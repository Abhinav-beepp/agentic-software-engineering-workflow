# Risks, Trade-offs and Validation

| Risk | Impact | Mitigation |
|---|---|---|
| SQLite write contention | Medium | PostgreSQL for production and horizontal scaling |
| Short-code collision | Low | Unique index and bounded retries |
| Analytics growth | Medium | Move events to an append-only/event pipeline at scale |
| Model-generated output can be incorrect | High | Deterministic validation, tests, guardrails, human approval |
| Arbitrary generated code execution | High | Do not execute untrusted generated code in this prototype |

## Validation strategy

Validation is layered: structured state checks, deterministic artifact checks, repository tests, and human approval. The test suite is the final executable correctness signal for the implementation.
