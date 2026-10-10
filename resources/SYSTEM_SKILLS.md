# System Skills — Agent Incident Analyzer

## 1. Purpose

This document defines the main skills of the Agent Incident Analyzer. Skills describe the system's functional capabilities and guide the orchestrator in selecting agents and executing the steps required to analyze an incident.

These are system capabilities, not IDE-specific skills.

## 2. Available Skills

### Skill 1 — Incident Classification

**Objective:** Understand the user's request and classify the incident.

**Responsibilities:**

* Identify the affected service, when provided.
* Identify reported symptoms, errors, and impacts.
* Determine which evidence sources should be consulted.
* Select the required specialized agents.

**Expected output:** Initial incident classification and investigation plan.

### Skill 2 — Evidence Collection

**Objective:** Collect operational evidence to investigate the incident.

**Responsibilities:**

* Retrieve recent logs and relevant errors.
* Check service and API status.
* Retrieve database-related information.
* Check recent deployments.
* Execute independent investigations in parallel when possible.

**Expected output:** Evidence organized by source.

### Skill 3 — Evidence Correlation

**Objective:** Correlate evidence collected by different agents.

**Responsibilities:**

* Identify temporal relationships between errors and deployments.
* Compare application symptoms with database indicators.
* Identify conflicting or insufficient evidence.
* Distinguish observed facts from hypotheses.

**Expected output:** Correlated evidence supporting the diagnosis.

### Skill 4 — Root Cause Analysis

**Objective:** Identify the most likely cause of the incident.

**Responsibilities:**

* Analyze the collected evidence.
* Formulate one or more hypotheses.
* Explain which evidence supports each hypothesis.
* Report the diagnosis confidence level.
* Identify cases where the available data is insufficient.

**Expected output:** Probable root cause, supporting evidence, and confidence level.

### Skill 5 — Action Recommendation

**Objective:** Recommend actions to investigate, mitigate, or resolve the incident.

**Responsibilities:**

* Recommend actions proportional to the available evidence.
* Prioritize diagnostic and mitigation steps.
* Explain the rationale behind each recommendation.
* Highlight relevant risks and required validations.

**Expected output:** Prioritized list of recommended actions.

This skill provides recommendations only. It does not execute changes in real systems.

### Skill 6 — Incident Reporting

**Objective:** Consolidate the investigation into a clear response for the user.

**Responsibilities:**

* Summarize the incident.
* Present relevant evidence.
* Explain the probable root cause.
* List recommended actions.
* Describe limitations and completed investigation steps.
* Provide the execution trace.

**Expected output:** Final incident analysis report.

## 3. Skill Orchestration

The orchestrator, implemented with LangGraph, determines which skills and agents are required for each request.

Conceptual workflow:

1. Classify the incident.
2. Select the relevant evidence sources.
3. Execute independent investigations in parallel when possible.
4. Correlate the results.
5. Analyze the probable root cause.
6. Recommend actions.
7. Consolidate the final response.

The workflow may vary depending on the request. Not every incident requires every evidence source.

## 4. Execution Principles

* Prioritize evidence relevant to the incident.
* Avoid unnecessary tool calls.
* Do not state a root cause without supporting evidence.
* Explicitly report insufficient data.
* Preserve investigation results and execution history.
* Handle tool failures appropriately.

## 5. Architectural Responsibilities

* **Orchestrator:** Selects and coordinates skills.
* **Agents:** Execute specialized tasks.
* **MCP:** Exposes tools for operational data access.
* **LLM:** Assists with interpretation, correlation, and hypothesis generation.
* **SQLite:** Stores simulated operational data.
* **FastAPI and Gradio:** Provide user interaction.
