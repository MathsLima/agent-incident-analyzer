# Architecture Rules

## Purpose

These rules define the architectural constraints of the Agent Incident Analyzer.

## Core Architecture

The system must maintain the following logical boundaries:

```text
User
  |
Gradio
  |
FastAPI
  |
Orchestrator / LangGraph
  |
Agents
  |
MCP Client
  |
MCP Server
  |
SQLite
```

The LLM provider is isolated behind the LLM layer.

## Responsibilities

### Orchestrator

The orchestrator is responsible for:

* Understanding the incident request.
* Selecting appropriate agents.
* Building the execution workflow.
* Executing independent agents in parallel when possible.
* Combining agent results.
* Sending consolidated evidence to downstream agents.
* Producing the final response.

The orchestrator must not directly query SQLite.

### Agents

Agents are responsible for domain-specific analysis.

Agents must not:

* Directly access SQLite.
* Implement database queries unrelated to their domain.
* Modify infrastructure.
* Execute shell commands for incident remediation.
* Contain orchestration logic belonging to LangGraph.

### MCP

MCP is the boundary between agents and operational data.

MCP tools should be:

* Read-only.
* Explicitly named.
* Small and focused.
* Easy to test.
* Safe to execute.

Agents should use MCP rather than directly accessing the database.

### Database

SQLite is only a simulated operational data source.

The database layer must not contain agent reasoning or orchestration logic.

### LLM

Provider-specific LLM code must remain isolated in:

```text
src/llm/
```

Agents should not contain provider-specific API implementation.

## Dynamic Workflow

The workflow must support different execution paths.

Example:

```text
ORCHESTRATOR
     |
     +---- API AGENT
     |
     +---- DATABASE AGENT
             |
             v
       ROOT CAUSE AGENT
             |
             v
        ACTION AGENT
```

The exact workflow should depend on the incident request.

Do not replace the dynamic orchestration with a permanently hard-coded sequence unless explicitly required for a test or fallback.

## Simplicity

This is an educational demonstration project.

Prefer:

* Small modules.
* Simple data structures.
* Clear interfaces.
* Minimal dependencies.
* Readable code.

Avoid unnecessary enterprise abstractions.

Do not introduce:

* Microservices.
* Message brokers.
* Kubernetes.
* Redis.
* Complex ORM architectures.
* Distributed tracing infrastructure.
* Production authentication systems.

unless explicitly requested.

## Secrets

Never hard-code:

* API keys.
* Tokens.
* Passwords.
* Credentials.

Use environment variables.

Never commit `.env`.

## Architectural Changes

If implementation requires a change to the architecture described in:

```text
docs/SPEC.md
docs/PLAN.md
```

stop and report the proposed change before implementing it.

Do not silently redefine the architecture.
