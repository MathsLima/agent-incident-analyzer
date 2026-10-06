# Agent Workflow Rules

## Source of Truth

Before implementing anything, read:

1. `docs/SPEC.md`
2. `docs/PLAN.md`
3. `docs/AGENT_GUIDELINES.md`
4. Relevant files under `agent/rules/`
5. Relevant files under `agent/skills/`

The specification defines what the system should do.

The plan defines the implementation sequence.

The rules define constraints.

The skills define execution procedures.

## Phase-Based Implementation

Implement one PLAN phase at a time.

Do not implement the entire project in one task.

At the beginning of a phase:

1. Inspect the current repository.
2. Identify what has already been implemented.
3. Read the relevant phase in `docs/PLAN.md`.
4. Identify dependencies from previous phases.

During the phase:

1. Implement only the required scope.
2. Run appropriate validation.
3. Fix problems found during validation.
4. Keep documentation consistent.

At the end:

1. Run tests.
2. Check imports.
3. Check for architectural violations.
4. Review changed files.
5. Report the phase status.
6. Stop.

## Mandatory Phase Report

Every completed phase must end with:

```text
Phase:
Status:

Implemented:
- ...

Files created:
- ...

Files modified:
- ...

Validation:
- ...

Tests:
- ...

Known issues:
- ...

Next phase:
- ...
```

## Stop Conditions

Stop implementation if:

* A required architectural decision is ambiguous.
* The specification conflicts with the implementation plan.
* A required external API is unclear.
* A dependency introduces unexpected compatibility problems.
* A change would significantly alter the architecture.

Report the problem instead of inventing a solution.

## Do Not Continue Automatically

Completing one phase does not authorize implementation of the next phase.

Wait for a new instruction.

## Git

Keep changes focused on the current phase.

Do not modify unrelated files.

Do not remove user code without justification.

Do not rewrite large parts of the repository when a small change is sufficient.
