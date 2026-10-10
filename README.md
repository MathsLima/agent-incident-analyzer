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
├── sdlc/
│   └── 01-app-creation/
│       ├── SPEC.md
│       └── PLAN.md
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
│   │   ├── app.py
│   │   ├── models.py
│   │   └── routes.py
│   ├── agents/
│   │   ├── base_agent.py
│   │   ├── log_agent.py
│   │   ├── api_agent.py
│   │   ├── database_agent.py
│   │   ├── deployment_agent.py
│   │   ├── root_cause_agent.py
│   │   └── action_agent.py
│   ├── database/
│   │   ├── connection.py
│   │   ├── schema.py
│   │   └── seed.py
│   ├── llm/
│   │   └── client.py
│   ├── mcp/
│   │   ├── server.py
│   │   └── tools.py
│   ├── orchestrator/
│   │   ├── graph.py
│   │   └── state.py
│   ├── ui/
│   │   └── gradio_app.py
│   └── config.py
│
├── scripts/
│   ├── check_config.py
│   └── seed_database.py
│
├── tests/
│
├── .devcontainer/
│   └── devcontainer.json
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

The specification and implementation plan are available under `sdlc/01-app-creation/`.

---

## Environment Setup

### Local Development

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

### GitHub Codespaces

Open the repository in GitHub Codespaces. The dev container will automatically:

1. Use Python 3.11
2. Install dependencies from `requirements.txt`
3. Forward ports 7860 (Gradio) and 8000 (FastAPI)

Inside the Codespace, create the `.env` file:

```bash
cp .env.example .env
```

Then configure the NVIDIA NIM credentials in `.env`.

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

### Step 1: Initialize the Database

```bash
python scripts/seed_database.py
```

This will create the SQLite database and populate it with demonstration data.

### Step 2: Start the Gradio Interface

```bash
python run.py
```

The Gradio interface will be available at http://localhost:7860

### Step 3: Start the FastAPI Server (Optional)

```bash
python run_api.py
```

The FastAPI API will be available at http://localhost:8000
API documentation will be available at http://localhost:8000/docs

### Step 4: Start the MCP Server (Optional)

```bash
python -m src.mcp.server
```

The MCP server will run using stdio transport for communication with MCP clients.

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

## Testing

### Configuration Test

```bash
python scripts/check_config.py
```

This verifies that the configuration module loads correctly.

### Integration Test

```bash
python scripts/test_integration.py
```

This tests database connection and MCP tools without requiring the LLM API key.

### Orchestrator Test

```bash
python scripts/test_orchestrator.py
```

This tests the full orchestrator workflow with the LLM. Requires NVIDIA_API_KEY to be configured.

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
