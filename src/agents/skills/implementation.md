# Implementation Skill

## Objective

Implement the requested phase from `docs/PLAN.md` while respecting the architecture and rules.

## Procedure

### Step 1 — Understand

Read:

* `docs/SPEC.md`
* `docs/PLAN.md`
* `docs/AGENT_GUIDELINES.md`
* Relevant architecture rules.

Identify:

* Required files.
* Required behavior.
* Dependencies.
* Expected validation.

### Step 2 — Inspect

Inspect the existing implementation before creating files.

Do not assume a file is missing because it was not explicitly mentioned in the task.

### Step 3 — Design

Choose the simplest implementation that satisfies the specification.

Avoid premature abstraction.

### Step 4 — Implement

Implement only the current phase.

Keep responsibilities separated according to the architecture rules.

### Step 5 — Validate

Run:

* Import checks.
* Relevant tests.
* Basic runtime checks.
* Configuration checks when applicable.

### Step 6 — Review

Verify:

* No secrets were introduced.
* No unrelated files were modified.
* Architecture boundaries are respected.
* Documentation remains consistent.

### Step 7 — Report

Provide the mandatory phase report defined in:

```text
agent/rules/workflow.md
```

Then stop.
