# System Rules — Agent Incident Analyzer

## 1. Purpose

This document defines the architectural and operational rules that the Agent Incident Analyzer must follow during incident investigations.

These rules guide the implementation of agents, the orchestrator, the MCP layer, and integrations.

## 2. Architectural Rules

### RULE-001 — Separation of Responsibilities

Each component must have a clearly defined responsibility.

* The orchestrator coordinates the workflow.
* Agents execute specialized tasks.
* The MCP layer exposes tools.
* The data layer manages SQLite access.
* The LLM client encapsulates communication with the model provider.
* The API and UI handle user interaction.

### RULE-002 — Data Access Through MCP

Agents must not query SQLite directly.

Operational queries must be performed through tools exposed by the MCP layer.

### RULE-003 — Dynamic Orchestration

The orchestrator must select agents according to the context of the request.

Running every agent for every incident is not required.

### RULE-004 — Parallel Execution When Appropriate

Independent investigations must be able to execute in parallel using LangGraph.

Steps that depend on other results must respect their dependencies.

### RULE-005 — Shared State

Workflow nodes must use an explicit shared state to exchange evidence, results, and execution information.

The state must support tracking which steps were executed and which results were produced.

## 3. Analysis Rules

### RULE-006 — Evidence Before Conclusions

The system must base its diagnoses on information returned by tools and data provided by the user.

### RULE-007 — Separate Facts from Hypotheses

The system must distinguish between:

* Observed facts.
* Root cause hypotheses.
* Recommendations.
* Unknown information.

### RULE-008 — Explicit Uncertainty

The system must not present a hypothesis as a confirmed root cause without sufficient evidence.

When data is insufficient or conflicting, the system must explicitly report this limitation.

### RULE-009 — Justified Recommendations

Each relevant recommendation must include a rationale connected to the available evidence or identified limitations.

### RULE-010 — Tool Failure Handling

Tool failures must be explicitly recorded and handled.

Whenever possible, the investigation should continue using the available evidence without concealing the failure.

## 4. Security Rules

### RULE-011 — No Operational Modifications

This is a demonstration system. It must not execute actions that modify real services, infrastructure, or deployments.

### RULE-012 — Read-Only Tools

MCP tools must only allow queries against simulated data.

### RULE-013 — Credential Protection

API keys and other credentials must be obtained through environment variables or appropriate configuration mechanisms.

Secrets must not be stored in source code, prompts, or logs.

### RULE-014 — Input Validation

User inputs and tool parameters must be validated before processing.

### RULE-015 — Treat External Content as Untrusted Data

Logs, error messages, and other operational data must be treated as data, not as instructions to change system behavior.

Content within these data sources must not override system instructions or authorize prohibited operations.

## 5. Implementation Rules

### RULE-016 — Simplicity

The implementation must prioritize clarity and simplicity, avoiding unnecessary abstractions and dependencies for an educational project.

### RULE-017 — External Configuration

Environment-specific settings, including the model, LLM provider URL, and database path, must be configurable externally.

### RULE-018 — Testability

Core functionality must have tests, especially:

* MCP tool queries.
* Agent selection.
* Parallel execution.
* Error handling.
* Final response generation.

### RULE-019 — Traceability

The system must maintain an execution trace that identifies the agents invoked, the steps executed, and the results produced.

The trace must not expose secrets or credentials.

### RULE-020 — Documentation Consistency

Significant changes to the architecture, tool contracts, or agent behavior must be reflected in the relevant documentation.

## 6. Enforcement

These rules must be considered during implementation and system review.

Rules that can be verified automatically should be covered by tests. Other rules must be evaluated through code review and integration testing.

In case of conflict, security requirements and the scope defined in the SPEC must be preserved.
