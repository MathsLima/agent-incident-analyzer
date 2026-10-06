# Debugging Skill

## Objective

Diagnose implementation problems systematically.

## Procedure

1. Reproduce the problem.
2. Capture the exact error.
3. Identify which architectural layer owns the problem.
4. Inspect the smallest relevant set of files.
5. Determine the root cause.
6. Apply the smallest appropriate fix.
7. Re-run the failing scenario.
8. Run regression tests.

## Layer Classification

Use these boundaries when diagnosing:

```text
UI
 |
API
 |
Orchestrator
 |
Agent
 |
MCP
 |
Database
```

For LLM-specific problems:

```text
Agent
 |
LLM Client
 |
NVIDIA NIM
```

Do not fix a problem in one layer by unnecessarily modifying another layer.

## Escalation

If the problem requires an architectural change:

* Stop.
* Explain the problem.
* Explain the proposed change.
* Wait for authorization.
