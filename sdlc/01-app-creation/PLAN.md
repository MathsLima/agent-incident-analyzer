# Agent Incident Analyzer

## Implementation Plan

## 1. Purpose

This document defines the implementation plan for the Agent Incident Analyzer.

The implementation will follow the system specification and will be performed incrementally.

Each phase should result in a functional and verifiable part of the system.

---

# 2. Development Strategy

The project will be developed in small increments.

The recommended implementation order is:

```text
1. Project foundation
2. Configuration
3. SQLite data layer
4. MCP server
5. LLM integration
6. Agent prompts
7. Individual agents
8. Shared agent state
9. LangGraph orchestrator
10. FastAPI
11. Gradio
12. Integration
13. Testing
14. Demo preparation
```

The system should remain runnable throughout development whenever possible.

---

# 3. Phase 1 — Project Foundation

## Objective

Create the repository structure and development configuration.

## Deliverables

```text
README.md
.gitignore
.env.example
requirements.txt

docs/
    SPEC.md
    PLAN.md

src/
    api/
    agents/
    database/
    llm/
    mcp/
    orchestrator/

prompts/
tests/
```

## Validation

The Python environment should be created and dependencies should install successfully.

---

# 4. Phase 2 — Configuration

## Objective

Create centralized configuration for the application.

Configuration should include:

```text
NVIDIA_API_KEY
NVIDIA_MODEL
NVIDIA_BASE_URL
DATABASE_URL
```

Secrets must be loaded from environment variables.

## Deliverables

```text
src/config.py
.env.example
```

## Validation

The application should be able to start without hard-coded secrets.

---

# 5. Phase 3 — SQLite Data Layer

## Objective

Create the simulated operational dataset.

## Deliverables

```text
src/database/
    connection.py
    schema.py
    seed.py
```

The database should contain:

```text
services
logs
deployments
incidents
metrics
```

## Validation

The seed process should create a local SQLite database containing realistic demonstration data.

---

# 6. Phase 4 — MCP Server

## Objective

Expose operational data through MCP tools.

Agents should not access SQLite directly.

## Deliverables

```text
src/mcp/
    server.py
    tools.py
```

Initial tools:

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

## Validation

The MCP server should start independently and its tools should return valid data.

---

# 7. Phase 5 — LLM Integration

## Objective

Create a reusable NVIDIA NIM client.

## Deliverables

```text
src/llm/
    client.py
```

The rest of the system should interact with a generic LLM interface rather than directly depending on NVIDIA-specific implementation details.

## Validation

A simple test request should successfully reach the configured NVIDIA NIM endpoint.

---

# 8. Phase 6 — Agent Prompts

## Objective

Create explicit system prompts for each agent.

## Deliverables

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

Each prompt should define:

* role
* responsibilities
* available information
* available tools
* expected output
* constraints

## Validation

Every agent should have a clear and independently understandable system prompt.

---

# 9. Phase 7 — Individual Agents

## Objective

Implement each specialized agent.

## Deliverables

```text
src/agents/
    log_agent.py
    api_agent.py
    database_agent.py
    deployment_agent.py
    root_cause_agent.py
    action_agent.py
```

Agents should be implemented independently from the final orchestration graph.

## Validation

Each agent should be testable independently.

---

# 10. Phase 8 — Shared State

## Objective

Define the state exchanged between agents.

The state should contain information such as:

```text
user_request
incident_type
selected_agents
logs
api_data
database_data
deployment_data
root_cause
confidence
recommended_actions
execution_trace
final_response
```

## Deliverables

```text
src/orchestrator/
    state.py
```

## Validation

Agents should be able to read and update the appropriate portions of shared state.

---

# 11. Phase 9 — LangGraph Orchestrator

## Objective

Implement the dynamic agent workflow.

## Deliverables

```text
src/orchestrator/
    graph.py
    orchestrator.py
```

The orchestrator should:

1. Receive the user request.
2. Analyze the request.
3. Determine relevant agents.
4. Build or route through the appropriate workflow.
5. Execute independent agents in parallel.
6. Collect their results.
7. Send evidence to Root Cause Agent.
8. Send the result to Action Agent.
9. Produce the final response.

## Example

Simple workflow:

```text
Orchestrator
    |
    v
API Agent
    |
    v
Root Cause
    |
    v
Action
```

Parallel workflow:

```text
              +---- API Agent -------+
              |                      |
Orchestrator -+---- Database Agent --+---- Root Cause
              |                      |
              +---- Log Agent -------+
```

## Validation

Different user requests should result in different execution paths.

---

# 12. Phase 10 — FastAPI

## Objective

Expose the agent system through an HTTP API.

## Deliverables

```text
src/api/
    app.py
    routes.py
    models.py
```

Initial endpoint:

```text
POST /chat
```

The API should accept a user message and return:

```text
response
execution_trace
```

## Validation

The endpoint should successfully execute the LangGraph workflow.

---

# 13. Phase 11 — Gradio

## Objective

Create a simple conversational interface.

## Deliverables

```text
src/ui/
    gradio_app.py
```

The interface should provide:

```text
Chat history
User input
Assistant response
Execution trace
```

## Validation

A user should be able to interact with the complete system through a browser.

---

# 14. Phase 12 — Integration

## Objective

Connect all system components.

Final architecture:

```text
                    +-----------+
                    |  Gradio   |
                    +-----+-----+
                          |
                          v
                    +-----------+
                    |  FastAPI  |
                    +-----+-----+
                          |
                          v
                    +-----------+
                    | LangGraph |
                    |   ORQ     |
                    +-----+-----+
                          |
             +------------+------------+
             |            |            |
             v            v            v
           Agent        Agent        Agent
             |            |            |
             +------------+------------+
                          |
                          v
                     MCP Client
                          |
                          v
                      MCP Server
                          |
                          v
                        SQLite
```

## Validation

The complete request lifecycle should work from Gradio to final response.

---

# 15. Phase 13 — Testing

## Objective

Verify individual components and complete workflows.

## Tests

The project should include tests for:

```text
Configuration
Database
MCP tools
LLM integration
Individual agents
Orchestrator
API
End-to-end workflow
```

## Example scenarios

### Scenario A

Input:

```text
The payments API is returning HTTP 500 errors.
```

Expected behavior:

```text
API Agent
    |
Root Cause Agent
    |
Action Agent
```

---

### Scenario B

Input:

```text
The API is slow and database timeouts are occurring.
```

Expected behavior:

```text
API Agent -----+
               |
               +---- Root Cause
               |
Database Agent-+
```

---

### Scenario C

Input:

```text
The system started failing after the latest deployment.
```

Expected behavior may include:

```text
Log Agent
API Agent
Deployment Agent
        |
        v
Root Cause
        |
        v
Action
```

---

# 16. Phase 14 — Demo Preparation

## Objective

Prepare the project for the technical presentation.

The demonstration should show the project in the following order:

```text
1. SPEC.md
2. PLAN.md
3. Architecture
4. Project structure
5. Agent prompts
6. MCP tools
7. LangGraph workflow
8. SQLite data
9. Gradio interface
10. Live request
11. Execution trace
12. Final response
```

---

# 17. Recommended Demo Requests

The final demonstration should use predefined requests that produce visibly different workflows.

### Demo 1 — Simple

```text
The payments API is returning HTTP 500 errors.
```

Expected:

```text
ORQ
 |
API
 |
Root Cause
 |
Action
 |
ORQ
```

---

### Demo 2 — Parallel

```text
The payments API is slow and users are receiving database timeout errors.
```

Expected:

```text
        +-- API -------+
ORQ ----+              +-- Root Cause -- Action -- ORQ
        +-- Database --+
```

---

### Demo 3 — Complex

```text
We started receiving many HTTP 500 errors immediately after the latest deployment and the database also appears to be unstable.
```

Expected to involve multiple investigation agents:

```text
             +-- Log --------+
             |               |
ORQ ---------+-- API --------+-- Root Cause -- Action -- ORQ
             |               |
             +-- Database ---+
             |
             +-- Deployment
```

The exact workflow will be determined by the orchestrator.

---

# 18. Definition of Done

The project is considered complete when:

* The system can be started locally.
* Gradio provides a working chat interface.
* FastAPI exposes the application API.
* NVIDIA NIM is used as the LLM provider.
* LangGraph manages the workflow.
* Multiple specialized agents exist.
* MCP exposes operational tools.
* SQLite contains simulated operational data.
* Agents do not directly depend on SQLite.
* The orchestrator dynamically selects agents.
* Independent agents can execute in parallel.
* Root Cause Agent consolidates investigation results.
* Action Agent generates recommendations.
* Execution traces can be inspected.
* At least three different incident scenarios produce different workflows.
* Documentation clearly explains the architecture.
* Prompts are stored separately from implementation.
* No secrets are committed to the repository.

---

# 19. Development Principle

The implementation should favor:

```text
Clarity
    >
Complexity
```

The project is a demonstration system.

Every architectural decision should be simple enough to explain during a technical presentation.

The implementation should avoid unnecessary abstractions, frameworks, or infrastructure that do not contribute directly to demonstrating agentic system development.
