# Testing Skill

## Objective

Validate that the implementation behaves correctly without unnecessarily testing implementation details.

## Procedure

1. Identify the functionality introduced or modified.
2. Locate existing tests.
3. Add focused tests when appropriate.
4. Run the relevant tests.
5. Run broader tests when changes affect shared components.
6. Check importability of modified modules.

## Test Priorities

Prefer testing:

* Pure functions.
* Configuration behavior.
* Database operations.
* MCP tool behavior.
* Agent behavior.
* Orchestrator state transitions.
* API endpoints.

## Failure Handling

When a test fails:

1. Read the complete error.
2. Identify the root cause.
3. Fix the implementation if the implementation is wrong.
4. Re-run the failed test.
5. Re-run related tests.

Do not disable or weaken tests merely to make the test suite pass.

## External Services

Tests should not require a real NVIDIA API key unless explicitly intended as an integration test.

Prefer mocks or deterministic local data for unit tests.

SQLite test data should remain isolated from development data.
