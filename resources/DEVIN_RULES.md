# Devin Rules — Agent Incident Analyzer

## 1. Purpose

These rules define the mandatory constraints for all development work performed by Devin in the Agent Incident Analyzer repository.

The project is an educational, locally runnable multi-agent system designed to demonstrate agent orchestration, tool integration, parallel execution, incident analysis, and an SDLC-oriented development workflow.

These rules apply to every implementation phase, code change, test, refactoring, and documentation update.

## 2. Source of Truth

Before modifying the repository, read the following documents:

1. `docs/SPEC.md` — functional and architectural requirements.
2. `docs/PLAN.md` — implementation phases and their order.
3. `docs/AGENT_GUIDELINES.md` — implementation workflow and reporting requirements.
4. `docs/DEVIN_RULES.md` — mandatory constraints.
5. `docs/DEVIN_SKILLS.md` — technical implementation procedures.
6. `docs/DEVIN_TOOLS.md` — development commands and application tool contracts.
7. `README.md` — setup and project overview.

When documents conflict, follow this precedence:

1. Explicit user instructions for the current task.
2. `docs/SPEC.md` for functional and architectural requirements.
3. `docs/PLAN.md` for implementation sequence.
4. These rules and the remaining project documentation.

If a conflict cannot be resolved safely, explain it and request clarification instead of silently making a significant architectural decision.

## 3. Phase-Based Development

* Implement only the phase explicitly authorized by the user.
* Review the current repository state before making changes.
* Do not reimplement components that already satisfy the requirements.
* Do not proceed to the next phase automatically.
* Complete the current phase, run appropriate validation, report the results, and stop.
* If a dependency from a future phase is genuinely required, explain why before expanding the scope.
* If a phase cannot be completed, report the blocker and the work that remains.

## 4. Architecture Boundaries

Preserve the separation of responsibilities:

* `src/api/`: HTTP endpoints and request/response handling.
* `src/agents/`: specialized incident-analysis agents.
* `src/orchestrator/`: shared workflow state and LangGraph orchestration.
* `src/mcp/`: MCP server, client integration, and application tool exposure.
* `src/database/`: SQLite connection management, schema, seed data, and data access.
* `src/llm/`: NVIDIA NIM integration and LLM client configuration.
* `src/ui/`: Gradio user interface, when introduced by the implementation plan.
* `prompts/`: system prompts and agent-specific instructions.
* `tests/`: automated tests.

Keep these boundaries consistent with the existing specification and plan. Do not introduce new architectural layers, services, or frameworks without a concrete requirement.

Agents must access operational data through the documented MCP tools rather than opening SQLite connections directly. Database connection management and SQL queries belong in the database and MCP layers.

The orchestrator coordinates agents and combines their outputs. It should not duplicate the internal logic of specialized agents.

## 5. Technology Constraints

Use the technologies specified in the project:

* Python
* FastAPI
* LangGraph
* MCP
* NVIDIA NIM
* Gradio
* SQLite

Use the existing dependency manifest as the starting point. Add, remove, or change dependencies only when justified by implementation requirements and library compatibility.

Prefer Python's standard library when it is sufficient. Avoid unnecessary abstractions, frameworks, and dependencies.

Do not replace a specified technology with an alternative without explicit approval.

## 6. Agent Orchestration

* The orchestrator must support selecting agents according to the incident request and available evidence.
* Independent investigation tasks should be eligible for parallel execution.
* Dependent tasks must execute only after their required inputs are available.
* All participating agents must use a clearly defined shared state or an explicitly documented input/output contract.
* Agent outputs must be structured and suitable for aggregation.
* The workflow must preserve an execution trace that explains which agents ran and what they contributed.
* The final response must distinguish observed evidence from inferred causes.
* Confidence values must not imply statistical calibration unless the implementation actually provides it.
* Do not create agents that have no clear responsibility or measurable contribution.

Do not implement a purely hard-coded workflow and describe it as dynamic orchestration. If deterministic routing is used as a fallback, document its limitations.

## 7. MCP and Data Access

* Expose application data through explicit, documented MCP tools.
* Follow the MCP SDK's supported API and lifecycle.
* Validate tool inputs and return predictable, structured outputs.
* Use read-only tools for operational investigation.
* Do not expose arbitrary SQL execution, shell execution, filesystem access, or destructive operations as incident-analysis tools.
* Do not implement real production integrations.
* Do not allow an LLM-generated tool argument to bypass input validation.
* Handle missing records, empty results, and tool errors explicitly.
* Keep database implementation details out of agent prompts unless they are relevant to a tool contract.

## 8. Security and Configuration

* Never hard-code API keys, passwords, or other secrets.
* Never print or expose the NVIDIA API key in logs, API responses, execution traces, or UI messages.
* Load configuration from environment variables and the local `.env` file when applicable.
* Keep `.env` out of version control.
* Maintain `.env.example` with placeholder values only.
* Never require a real production credential to run offline tests.
* Validate required configuration clearly and fail with actionable error messages.
* Do not log sensitive environment values.

## 9. Database and Demonstration Data

* Use SQLite and synthetic data for the demonstration.
* Keep schema creation and seed-data initialization repeatable.
* Avoid inserting duplicate seed records on every startup.
* Do not depend on a real monitoring platform, cloud account, production database, or external incident-management system.
* Keep demonstration data representative enough to support log, API, database, service, and deployment investigations.
* Make the application usable without access to real infrastructure.

## 10. Code Quality

* Use clear names, type hints, and focused functions.
* Keep modules small enough to understand during a code walkthrough.
* Prefer explicit control flow over unnecessary metaprogramming.
* Avoid circular imports.
* Avoid broad exception handling that silently hides failures.
* Do not use placeholder implementations while claiming a feature is complete.
* Do not leave unexplained `TODO` markers in functionality declared complete.
* Use asynchronous code only where it is useful and compatible with the relevant libraries.
* Preserve compatibility with the project's documented Python environment.

## 11. Testing and Validation

For every phase:

* Run the relevant automated tests.
* Validate imports and basic startup paths where applicable.
* Test failure paths as well as successful execution.
* Use mocks or synthetic data when external services are not required.
* Do not make successful test claims unless the tests were actually executed.
* Report tests that could not run and explain why.
* Fix regressions introduced by the current changes before declaring the phase complete.

Tests must not require a real NVIDIA API key unless the test is explicitly designated as an integration test and the requirement is documented.

## 12. Documentation and Repository Hygiene

* Update documentation when implementation details or commands change.
* Keep `README.md`, `.env.example`, `requirements.txt`, and the implementation consistent.
* Do not commit local databases, virtual environments, secrets, caches, or generated artifacts.
* Do not delete user-created files or rewrite unrelated work.
* Avoid broad refactoring during a narrowly scoped phase.
* Use the existing directory structure unless a documented requirement justifies a change.

## 13. Definition of Done

A phase is complete only when:

1. Its planned deliverables have been implemented.
2. The implementation matches the specification.
3. Relevant tests and validations have been run.
4. Known limitations are documented.
5. Required documentation is updated.
6. No unrelated phase has been silently implemented.
7. A completion report has been provided.

## 14. Required Completion Report

At the end of each phase, provide:

* **Phase:** phase number and name.
* **Status:** completed, partially completed, or blocked.
* **Implemented:** concise summary of behavior delivered.
* **Files created:** all new files.
* **Files modified:** all changed files.
* **Validation:** commands executed and their actual results.
* **Tests:** passed, failed, and not executed.
* **Known issues:** limitations, compatibility concerns, and outstanding work.
* **Next phase:** the next planned phase, without implementing it.

Stop after providing the report and wait for explicit authorization to continue.