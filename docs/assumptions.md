# Assumptions and Limitations

## Assumptions

- The mandatory analytics requirement means basic click analytics.
- The service does not require authentication unless specified by a future requirement.
- Local SQLite is acceptable for an interview demonstration.
- The requirement does not specify SLO, traffic, retention, or privacy requirements, so those are surfaced as ambiguities rather than silently invented.

## Limitations

- No distributed cache.
- No authentication/rate limiting/abuse controls in the mandatory service.
- No advanced analytics aggregation.
- No sandbox for executing arbitrary generated source code.
