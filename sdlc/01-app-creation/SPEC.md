# Agent Incident Analyzer

## 1. Overview

Agent Incident Analyzer is a small agentic system designed to demonstrate how a multi-agent system can receive a user request, understand the incident, dynamically select specialized agents, execute independent tasks in parallel, combine their results, and produce a final response.

The system will simulate an IT incident analysis environment using artificial operational data stored in SQLite.

The primary goal is not to build a production-ready incident management platform. The goal is to provide a simple, functional, and easily understandable reference implementation for demonstrating the architecture and development lifecycle of an agentic system.

The system will use:

* Python
* FastAPI
* Gradio
* LangGraph
* MCP
* NVIDIA NIM
* SQLite

---

## 2. Problem Statement

When an IT incident occurs, different sources of information may need to be analyzed before determining a probable root cause.

For example, an incident involving HTTP 500 errors may require analysis of:

* application logs
* API status
* database status
* recent deployments
* service metrics

A traditional application could implement a fixed sequence of checks.

This project demonstrates an agentic alternative where an orchestrator uses an LLM to determine which specialized agents should participate in the investigation based on the user's request.

---

## 3. Goals

The system must demonstrate the following concepts:

1. LLM-based orchestration.
2. Multiple specialized agents.
3. Dynamic agent selection.
4. Parallel execution of independent agents.
5. Sequential execution when an agent depends on previous results.
6. Shared state between agents.
7. MCP-based tool access.
8. Separation between agents and data sources.
9. Structured agent system prompts.
10. A visible workflow that can be explained during a technical presentation.
11. A simple conversational interface.
12. A development process based on specification and implementation planning.

---

## 4. Non-Goals

The system will not attempt to provide:

* real production monitoring
* real infrastructure access
* real cloud integrations
* real incident remediation
* production-grade authentication
* production-grade authorization
* distributed deployment
* persistent conversation management
* advanced observability infrastructure
* real-time monitoring

All operational data will be simulated.

---

## 5. User Experience

The user interacts with the system through a Gradio chat interface.

The user sends a natural-language incident description.

Example:

> The payments API started returning HTTP 500 errors after the latest deployment.

The system analyzes the request and determines which agents are relevant.

The system may execute a workflow similar to:

```text
User
  |
  v
Orchestrator
  |
  +----> Log Agent
  |
  +----> API Agent
  |
  +----> Deployment Agent
            |
            v
       Root Cause Agent
            |
            v
        Action Agent
            |
            v
       Orchestrator
            |
            v
           User
```

The actual workflow must be dynamically determined according to the incident.

---

## 6. Example Requests

### Example 1 — API incident

User:

> The payments API is returning HTTP 500 errors.

Possible workflow:

```text
Orchestrator
    |
    v
API Agent
    |
    v
Root Cause Agent
    |
    v
Action Agent
    |
    v
Orchestrator
```

---

### Example 2 — Database incident

User:

> The API is slow and users are getting database timeout errors.

Possible workflow:

```text
                 +----> API Agent -------+
                 |                       |
Orchestrator ----+                       +----> Root Cause Agent
                 |                       |
                 +----> Database Agent --+
                                             |
                                             v
                                        Action Agent
                                             |
                                             v
                                        Orchestrator
```

---

### Example 3 — Deployment-related incident

User:

> We started receiving many 500 errors immediately after the latest deployment.

Possible workflow:

```text
                  +----> Log Agent -----------+
                  |                            |
Orchestrator -----+----> API Agent ------------+----> Root Cause Agent
                  |                            |
                  +----> Deployment Agent -----+
                                                       |
                                                       v
                                                  Action Agent
                                                       |
                                                       v
                                                  Orchestrator
```

These workflows are examples. The orchestrator is responsible for determining the appropriate execution path.

---

## 7. System Architecture

The high-level architecture is:

```text
+------------------+
|      Gradio      |
|  Chat Interface  |
+--------+---------+
         |
         v
+------------------+
|     FastAPI      |
|    API Layer     |
+--------+---------+
         |
         v
+------------------+
|    LangGraph     |
|   Orchestrator   |
+--------+---------+
         |
         +-------------------+
         |                   |
         v                   v
+----------------+   +----------------+
|     Agents     |   | Shared State   |
+--------+-------+   +----------------+
         |
         v
+----------------+
|   MCP Client   |
+--------+-------+
         |
         v
+----------------+
|   MCP Server   |
+--------+-------+
         |
         v
+----------------+
|     SQLite     |
+----------------+
```

---

## 8. Agents

The initial system will contain the following agents.

### 8.1 Orchestrator

Responsible for:

* receiving the user request
* understanding the incident
* determining which agents are relevant
* creating the execution workflow
* coordinating agent execution
* maintaining shared state
* deciding when enough information has been collected
* producing or requesting the final response

The orchestrator is implemented using LangGraph.

---

### 8.2 Log Agent

Responsible for analyzing application and infrastructure logs.

It may use MCP tools such as:

```text
get_recent_logs()
search_logs()
```

The agent should identify relevant errors, patterns, and timestamps.

---

### 8.3 API Agent

Responsible for analyzing API and service information.

Example tools:

```text
get_service_status()
get_api_errors()
get_service_metrics()
```

---

### 8.4 Database Agent

Responsible for investigating database-related problems.

Example tools:

```text
get_database_status()
get_database_errors()
get_database_metrics()
```

---

### 8.5 Deployment Agent

Responsible for analyzing recent deployments and determining whether an incident may be correlated with a deployment.

Example tools:

```text
get_recent_deployments()
get_deployment_details()
```

---

### 8.6 Root Cause Agent

Responsible for analyzing the results produced by the investigation agents.

It does not directly investigate the database, API, or logs.

Instead, it receives the collected evidence and determines:

* probable root cause
* supporting evidence
* confidence
* affected services

---

### 8.7 Action Agent

Responsible for generating recommended next actions based on the identified root cause.

It should not execute destructive or real remediation actions.

The output should contain recommendations only.

---

## 9. Agent State

The LangGraph workflow will maintain a shared state.

Conceptually:

```text
IncidentState

- user_request
- incident_type
- selected_agents
- logs
- api_data
- database_data
- deployment_data
- root_cause
- confidence
- recommended_actions
- execution_trace
- final_response
```

The exact implementation may evolve during development.

---

## 10. MCP

MCP will be used to expose operational capabilities to agents as tools.

The agents should not directly depend on SQLite implementation details.

The conceptual architecture is:

```text
Agent
  |
  v
MCP Client
  |
  v
MCP Server
  |
  +---- Tool
  |
  +---- Tool
  |
  +---- Tool
  |
  v
SQLite
```

Example MCP tools:

```text
get_recent_logs
search_logs
get_service_status
get_api_errors
get_database_status
get_database_errors
get_recent_deployments
get_deployment_details
```

The initial MCP server will operate locally.

---

## 11. Data Model

SQLite will contain simulated operational information.

The initial logical entities are:

```text
services
logs
deployments
incidents
metrics
```

The database will contain predefined scenarios that allow the system to produce meaningful demonstrations.

Example:

```text
Service:
payments-api

Status:
degraded

Deployment:
version 2.4.1

Recent errors:
HTTP 500
DatabaseConnectionTimeout
ConnectionPoolExhausted
```

---

## 12. LLM

The system will use NVIDIA NIM as the LLM provider.

The LLM integration must be isolated from the rest of the application.

Configuration should be provided through environment variables.

Example:

```text
NVIDIA_API_KEY=
NVIDIA_MODEL=
NVIDIA_BASE_URL=
```

Secrets must never be committed to the repository.

---

## 13. Prompts

Each agent must have an explicit system prompt.

Prompts will be stored separately from Python implementation code.

Example structure:

```text
prompts/
    orchestrator.md
    log_agent.md
    api_agent.md
    database_agent.md
    deployment_agent.md
    root_cause_agent.md
    action_agent.md
```

This allows the prompts to be inspected and explained independently during the presentation.

---

## 14. Dynamic Workflow

The system must support different execution paths.

The workflow should not always execute every agent.

For example:

```text
Simple request:

Orchestrator
    |
    v
API Agent
    |
    v
Root Cause Agent
    |
    v
Action Agent
```

More complex request:

```text
                 +----> Log Agent -------+
                 |                        |
Orchestrator ----+----> API Agent --------+----> Root Cause
                 |                        |
                 +----> Database Agent ---+
```

The implementation should use LangGraph to represent these dependencies.

Independent agents should be executed in parallel whenever possible.

---

## 15. Execution Trace

The system should maintain an execution trace that can be displayed or logged.

Example:

```text
[ORCHESTRATOR] Incident received
[ORCHESTRATOR] Selected agents: API, Database
[API_AGENT] Started
[DATABASE_AGENT] Started
[API_AGENT] Completed
[DATABASE_AGENT] Completed
[ROOT_CAUSE_AGENT] Started
[ROOT_CAUSE_AGENT] Completed
[ACTION_AGENT] Started
[ACTION_AGENT] Completed
[ORCHESTRATOR] Final response generated
```

This is important for demonstrating how the agentic workflow operates.

---

## 16. API

FastAPI will provide the application API.

The initial API should expose a simple endpoint for incident analysis.

Conceptually:

```text
POST /chat
```

Request:

```json
{
  "message": "The payments API is returning HTTP 500 errors."
}
```

Response:

```json
{
  "response": "...",
  "execution_trace": []
}
```

The exact API contract will be defined during implementation.

---

## 17. Gradio

Gradio will provide the user-facing interface.

The interface should contain:

* chat history
* user input
* assistant response
* optional execution trace

The interface should remain intentionally simple.

The goal is to demonstrate the agent system, not frontend development.

---

## 18. Error Handling

The system should handle:

* invalid user requests
* unavailable LLM
* invalid agent output
* MCP tool errors
* database errors
* unexpected workflow errors

Errors should be represented in a controlled way and should not expose secrets.

---

## 19. Security

The project is a local demonstration system.

Nevertheless:

* API keys must be stored in environment variables.
* `.env` must not be committed.
* No secrets should appear in prompts or source code.
* MCP tools should only expose safe read operations.
* Agents must not execute real infrastructure commands.
* Action Agent must produce recommendations only.

---

## 20. Success Criteria

The project is considered successful when a user can:

1. Start the application locally.
2. Open the Gradio interface.
3. Submit an incident description.
4. Have the orchestrator determine relevant agents.
5. Execute multiple agents.
6. Execute independent agents in parallel.
7. Use MCP tools to retrieve simulated operational data.
8. Analyze the collected evidence.
9. Produce a probable root cause.
10. Generate recommended actions.
11. Receive a final natural-language response.
12. Inspect the execution trace.
13. Navigate through the project's specification, plan, prompts, agents, MCP implementation, and LangGraph workflow.

---

## 21. Demonstration Objective

The final demonstration should make it possible to explain the complete lifecycle of an agentic system:

```text
Requirement
     |
     v
Specification
     |
     v
Implementation Plan
     |
     v
Architecture
     |
     v
Agents + Tools
     |
     v
Orchestration
     |
     v
Execution
     |
     v
Final Response
```

The project should prioritize clarity and educational value over production complexity.
