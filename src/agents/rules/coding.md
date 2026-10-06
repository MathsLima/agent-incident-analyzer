# Coding Rules

## General

Write simple, readable Python.

Prefer clarity over cleverness.

Use type hints whenever practical.

Use small functions with clear responsibilities.

Avoid duplicated logic.

Avoid unnecessary abstractions.

## Project Structure

Respect the existing structure:

```text
src/
├── api/
├── agents/
├── database/
├── llm/
├── mcp/
└── orchestrator/
```

Create new directories only when they are justified by the specification or implementation plan.

## Error Handling

Do not silently swallow exceptions.

Bad:

```python
try:
    ...
except Exception:
    pass
```

Prefer explicit error handling with useful messages.

Errors should preserve enough context for debugging.

## Configuration

Configuration must come from environment variables or application configuration.

Never hard-code secrets.

## Dependencies

Before adding a dependency:

1. Check whether the existing dependencies already solve the problem.
2. Determine whether the dependency is actually necessary.
3. Prefer the simplest solution.

Do not add libraries only for convenience.

## Comments

Comments should explain:

* Why something exists.
* Important architectural decisions.
* Non-obvious behavior.

Do not add comments that merely restate the code.

## Logging

Use Python logging for application diagnostics.

Do not use scattered `print()` statements as the application's primary logging mechanism.

## Testing

New functionality should have an appropriate test when practical.

Tests should focus on behavior rather than implementation details.

## Backwards Compatibility

Do not unnecessarily break previously implemented phases.

When modifying existing functionality, run the relevant tests again.

## Documentation

If implementation changes behavior described in the documentation, update the relevant documentation.

Do not allow SPEC, PLAN, README, and implementation to silently diverge.
