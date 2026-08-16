# Example Scenario 1 — Greenfield

## Input

> Build a scalable URL shortener service with APIs, persistence, and analytics.

**Mode:** `greenfield`

## 1. Requirement analysis

The Requirement Agent normalizes the requirement into:

- **Functional:** create short URLs, persist mappings, redirect short codes, record click analytics.
- **Non-functional:** low-latency redirects, durable persistence, clear scaling path.
- **Ambiguities:** peak traffic, availability SLO, analytics retention/privacy, authentication, rate limits, expiration and custom aliases.
- **Acceptance criteria:** valid URLs can be shortened and persisted; redirects resolve and increment analytics; invalid/unknown inputs fail predictably; unit/integration tests cover core behavior.

The system does not silently invent unspecified requirements. It records them as assumptions or clarifying questions.

## 2. Task decomposition

```text
analysis
   |
   v
architecture
   |------------------|
   v                  v
api                database
   |                  |
   +--------+---------+
            v
     implementation
            |
            v
          tests
          /   \
         v     v
      risks  validation
               |
               v
            approval
               |
               v
            summary
```

The API and database tasks are independent after architecture and are eligible for concurrent execution.

## 3. Multi-step orchestration

The orchestrator records every transition in workflow history, including:

- task status
- dependencies
- execution order
- retry count
- outputs
- validation result
- approval decision

A task cannot run until all declared dependencies are `COMPLETED`.

## 4. Generated artifacts

The workflow produces:

| Artifact | Purpose |
|---|---|
| `implementation_plan.md` | implementation scope and rationale |
| `architecture.md` | architecture and data-flow decisions |
| `api_contract.json` | endpoint/request/response contract |
| `database_schema.md` | persistence design |
| `generated_code.py` | representative generated implementation artifact |
| `generated_tests.py` | representative generated test artifact |
| `test_plan.md` | test strategy |
| `risks-and-tradeoffs.md` | risks, mitigations and trade-offs |

The repository also contains the real runnable URL-shortener implementation under `src/app/`.

## 5. Validation

Deterministic validation checks:

- required workflow tasks exist;
- requirement analysis has acceptance criteria;
- architecture exists;
- generated artifacts exist on disk;
- API contract exists;
- test plan exists;
- runnable application entrypoint exists.

The repository test suite then validates the actual application and orchestration behavior.

## 6. Final output

The final engineering summary contains:

- implementation plan and rationale;
- architecture;
- generated artifacts;
- validation checks/results;
- risks;
- trade-offs;
- assumptions;
- limitations.

See `examples/output/greenfield.json` for a captured run produced by the workflow.
