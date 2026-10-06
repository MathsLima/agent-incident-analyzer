# Agent Incident Analyzer

A small multi-agent system designed to demonstrate the development and execution of an agentic architecture for IT incident analysis.

The system receives an incident description from a user, dynamically determines which specialized agents should participate in the investigation, executes independent tasks in parallel when possible, consolidates the collected evidence, identifies a probable root cause, and generates recommended actions.

The project is intentionally small and focused on demonstrating agentic system architecture rather than building a production-ready incident management platform.

---

## Architecture

The system is built around the following components:

```text
User
  |
  v
Gradio
  |
  v
FastAPI
  |
  v
LangGraph Orchestrator
  |
  +---- Log Agent
  |
  +---- API Agent
  |
  +---- Database Agent
  |
  +---- Deployment Agent
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

Operational information is exposed to agents through MCP tools:

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

## Technologies

* Python
* FastAPI
* Gradio
* LangGraph
* MCP
* NVIDIA NIM
* SQLite

---

## Project Structure

```text
agent-incident-analyzer/
│
├── docs/
│   ├── SPEC.md
│   └── PLAN.md
│
├── prompts/
│   ├── orchestrator.md
│   ├── log_agent.md
│   ├── api_agent.md
│   ├── database_agent.md
│   ├── deployment_agent.md
│   ├── root_cause_agent.md
│   └── action_agent.md
│
├── src/
│   ├── api/
│   ├── agents/
│   ├── database/
│   ├── llm/
│   ├── mcp/
│   └── orchestrator/
│
├── tests/
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Development Approach

The project follows a simplified SDLC process.

```text
Specification
      |
      v
Implementation Plan
      |
      v
Architecture
      |
      v
Implementation
      |
      v
Testing
      |
      v
Demonstration
```

The specification and implementation plan are available under `docs/`.

---

## Environment Setup

Create a Python virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Then configure the NVIDIA NIM credentials.

Never commit `.env` to the repository.

---

## Running the Application

The exact startup commands will be defined as implementation progresses.

The final application will provide:

* FastAPI API
* Gradio interface
* MCP server
* LangGraph orchestration

---

## Example Requests

### Simple API incident

```text
The payments API is returning HTTP 500 errors.
```

### Database incident

```text
The API is slow and users are receiving database timeout errors.
```

### Deployment incident

```text
We started receiving many HTTP 500 errors immediately after the latest deployment.
```

Different requests should result in different agent workflows.

---

## Project Objective

The main objective is educational.

The project demonstrates:

* agent orchestration
* dynamic routing
* parallel agent execution
* shared agent state
* MCP tools
* LLM integration
* LangGraph workflows
* separation between agents and data sources
* SDLC-driven agentic system development
