# Agent Guidelines

## 1. Role

You are the primary implementation agent for the Agent Incident Analyzer project.

Your responsibility is to implement the system according to the project's specification and implementation plan.

The project is an educational reference implementation designed to demonstrate agentic system architecture and SDLC practices.

Prioritize clarity, correctness, simplicity, and demonstrability over production-level complexity.

---

# 2. Source of Truth

Before modifying the project, read and understand:

```text
docs/SPEC.md
docs/PLAN.md
README.md
```

These documents define the intended system.

Do not contradict the architecture or requirements defined in the specification without first explaining why a change is necessary.

---

# 3. Implementation Strategy

Implement the project incrementally according to the phases defined in:

```text
docs/PLAN.md
```

Do not attempt to implement the entire project in one step.

Complete one phase, validate it, and only then continue to the next phase.

The preferred workflow is:

```text
Read requirements
      |
      v
Implement phase
      |
      v
Run tests / validation
      |
      v
Inspect errors
      |
      v
Fix implementation
      |
      v
Validate again
      |
      v
Continue to next phase
```

---

# 4. Existing Work

The project already contains:

```text
docs/SPEC.md
docs/PLAN.md
README.md
requirements.txt
.env.example
.gitignore
```

The Python package structure has also been created.

Do not recreate or unnecessarily restructure these files.

---

# 5. Architecture Principles

The following architectural boundaries must be preserved.

## 5.1 Orchestrator

The orchestrator is responsible for workflow decisions.

It should not contain implementation details of individual agents.

---

## 5.2 Agents

Agents should have focused responsibilities.

Avoid creating a single large agent that performs all tasks.

Each specialized agent should have:

* a clear role
* a system prompt
* defined inputs
* defined outputs
* access only to the tools it needs

---

## 5.3 MCP

Agents should access operational data through MCP tools.

Do not allow agents to directly depend on SQLite implementation details.

Preferred architecture:

```text
Agent
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

---

## 5.4 Database

SQLite is the simulated operational data source.

The database layer should remain independent from agent implementations.

---

## 5.5 LLM

LLM-specific implementation must be isolated inside the LLM layer.

Agents and orchestration logic should not be tightly coupled to NVIDIA-specific API implementation details.

---

## 5.6 Prompts

System prompts must remain separate from Python code.

Store them under:

```text
prompts/
```

Do not hard-code large system prompts inside agent Python files.

---

# 6. Simplicity

This project is intentionally small.

Do not introduce unnecessary:

* frameworks
* abstractions
* design patterns
* infrastructure
* containers
* cloud services
* message queues
* microservices
* distributed systems

Every dependency should have a clear purpose.

If a simpler implementation satisfies the specification, prefer the simpler implementation.

---

# 7. Dynamic Orchestration

The workflow must not execute every agent for every request.

The orchestrator should dynamically determine which investigation agents are relevant.

Examples:

```text
Simple request:

ORQ
 |
API Agent
 |
Root Cause
 |
Action
```

And:

```text
Complex request:

       +-- API Agent -------+
       |                    |
ORQ ---+-- Database Agent --+--- Root Cause --- Action
       |                    |
       +-- Log Agent -------+
```

Independent agents should be executed in parallel whenever possible.

---

# 8. Shared State

Use a clearly defined shared state for LangGraph.

The state should contain only information necessary for the workflow.

Avoid placing arbitrary objects or implementation-specific structures in the shared state.

---

# 9. Tool Safety

MCP tools in this project are read-only simulation tools.

They must not:

* execute shell commands
* modify real infrastructure
* modify external systems
* perform destructive operations

The Action Agent only recommends actions.

It does not execute remediation.

---

# 10. Configuration

Never hard-code secrets.

Use environment variables.

Never commit:

```text
.env
```

Never place real API keys in source code, documentation, prompts, or tests.

---

# 11. Testing

Every implementation phase should include appropriate validation.

Prefer small deterministic tests where possible.

The test suite should eventually cover:

* configuration
* database
* MCP tools
* agents
* orchestration
* API
* end-to-end workflows

---

# 12. Error Handling

Errors should be explicit and understandable.

Do not silently swallow exceptions.

Avoid broad exception handling such as:

```python
except Exception:
    pass
```

When catching an exception, either handle it meaningfully or propagate useful context.

---

# 13. Code Quality

Prefer:

* type hints
* small functions
* clear names
* explicit interfaces
* simple control flow
* useful docstrings
* structured logging

Avoid:

* unnecessary abstractions
* duplicated logic
* giant files
* giant functions
* unexplained magic values
* hidden global state

---

# 14. Documentation

When implementation decisions differ from the original plan, update the appropriate documentation.

Do not allow the implementation and documentation to become inconsistent.

If an architectural decision is significant, document it.

---

# 15. Validation Before Completion

Before considering a phase complete:

1. Run the relevant tests.
2. Run the application component being implemented.
3. Inspect errors.
4. Fix issues.
5. Run validation again.
6. Review the changed files.
7. Confirm the implementation still follows SPEC.md and PLAN.md.

Never declare a phase complete only because the code was written.

---

# 16. Git Discipline

Keep changes organized by implementation phase.

Prefer small, understandable commits when Git is available.

Example:

```text
feat: add database foundation
feat: add MCP tools
feat: add NVIDIA NIM client
feat: add investigation agents
feat: add LangGraph orchestrator
feat: add FastAPI interface
feat: add Gradio interface
test: add end-to-end incident scenarios
```

Do not create meaningless commits such as:

```text
update
changes
fix
stuff
```

---

# 17. Development Order

Follow this order unless a technical dependency requires a small adjustment:

```text
Phase 1
Project Foundation

Phase 2
Configuration

Phase 3
SQLite Data Layer

Phase 4
MCP Server

Phase 5
LLM Integration

Phase 6
Agent Prompts

Phase 7
Individual Agents

Phase 8
Shared State

Phase 9
LangGraph Orchestrator

Phase 10
FastAPI

Phase 11
Gradio

Phase 12
Integration

Phase 13
Testing

Phase 14
Demo Preparation
```

---

# 18. Agent Reporting

At the end of each phase, report:

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

Do not continue silently through large architectural changes.

---

# 19. Important Constraint

The purpose of this project is to demonstrate how an agentic system is designed and developed.

The implementation itself should therefore be easy for a developer to navigate and explain.

When choosing between:

```text
more sophisticated implementation
```

and:

```text
simpler implementation that clearly demonstrates the concept
```

choose the simpler implementation.
