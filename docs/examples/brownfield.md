# Example Scenario 2 — Brownfield

## Input

> Add rate limiting and API-key authentication to the existing URL shortener.

**Mode:** `brownfield`

## 1. Codebase reconnaissance

The Brownfield Agent scans the supplied repository and reports only files actually observed. It identifies relevant source, configuration and test files before proposing changes.

Typical observed impact areas in this repository include:

- `src/app/api/` — HTTP boundary and request handling
- `src/app/services/` — application/service logic
- `src/app/storage/` — persistence boundary
- `src/app/config.py` — configuration
- `tests/` — regression and integration coverage

The scanner does **not** claim to know architecture that it cannot observe.

## 2. Task decomposition

```text
brownfield_scan
      |
      v
analysis
      |
      v
architecture
   /       \
  v         v
api      database/config impact
  \         /
   \       /
    v     v
 implementation
       |
       v
     tests
       |
       v
     risks
       |
       v
   validation
       |
       v
    approval
       |
       v
    summary
```

The planner uses scan evidence as input to identify impacted modules and regression-test areas.

## 3. Multi-step orchestration

The workflow coordinates reconnaissance, analysis, architecture, API/security planning, implementation, testing, risk analysis, validation and approval. Dependencies prevent implementation from running before the impact analysis and design are complete.

## 4. Expected engineering outputs

The output should identify:

- authentication middleware/dependency;
- API-key configuration and secure secret handling;
- rate-limit policy and enforcement point;
- persistence changes only if required by the chosen design;
- affected tests;
- operational risks such as key leakage and false-positive throttling.

## 5. Validation

Validation checks both workflow/artifact completeness and the repository test suite. A brownfield run also requires the `brownfield_scan` task and confirms that it completed successfully.

See `examples/output/brownfield.json` for a captured workflow run.
