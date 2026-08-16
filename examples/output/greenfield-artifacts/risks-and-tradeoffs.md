# Risks and Trade-offs

- SQLite is demo-friendly but not a high-scale production datastore.
- Short-code collisions are handled with a uniqueness constraint and bounded retry.
- Analytics are intentionally basic for the prototype.
- Model-generated output can be wrong, so deterministic validation, tests, and human approval remain authoritative.
- The prototype never blindly executes arbitrary generated source code.
