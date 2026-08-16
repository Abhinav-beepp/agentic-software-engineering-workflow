# Example Scenario 3 — Ambiguous

## Input

> Make the URL service faster and more scalable.

**Mode:** `ambiguous`

## 1. Ambiguity detection

The Requirement Agent explicitly identifies missing information rather than pretending the target is precise.

### Ambiguities detected

1. Peak requests per second are unspecified.
2. Read/write ratio is unspecified.
3. Latency SLO is unspecified.
4. Availability target is unspecified.
5. Geographic distribution is unspecified.
6. Analytics retention and volume are unspecified.
7. Required security/rate-limit constraints are unspecified.

### Clarifying questions

- What peak RPS should be supported?
- What p95 redirect latency is required?
- What availability target is required?
- Is multi-region deployment required?
- What analytics retention period is required?
- Are authentication and rate limiting in scope?

### Provisional assumptions

For a prototype planning pass, the agent can proceed with explicit assumptions such as:

- single-region deployment;
- SQLite locally;
- basic click analytics;
- no authentication unless subsequently requested.

The important behavior is that assumptions are **visible and revisable**.

## 2. Task decomposition

The workflow still creates an actionable plan:

```text
analysis + ambiguity/questions
            |
            v
      architecture options
            |
            +----------------+
            |                |
            v                v
       API impact      persistence/cache impact
            \                /
             \              /
              v            v
               implementation plan
                       |
                       v
                     tests
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

## 3. Output validation

The validator ensures that the requirement analysis contains acceptance criteria and that the engineering workflow still produces the required artifacts. Human approval provides the final control point before the summary is finalized.

See `examples/output/ambiguous.json` for a captured workflow run.
