# System Tools — Agent Incident Analyzer

## 1. Purpose

This document defines the tools that agents can use to retrieve operational information during incident investigations.

Tools are exposed through the MCP layer and query simulated data stored in SQLite.

## 2. Design Principles

* Each tool must have a clear responsibility.
* Tools must perform read-only operations.
* Agents must not access SQLite directly.
* Input parameters must be validated.
* Tool responses must follow predictable structures.
* Query errors must be handled without unnecessarily interrupting the entire investigation.

## 3. Available Tools

### `get_service_status`

**Purpose:** Retrieve the current status of a service.

Parameters:

* `service_name`: Name of the service.

Expected response:

* Service name.
* Current status.
* Available information about its operational condition.

### `search_logs`

**Purpose:** Search logs associated with a service.

Parameters:

* `service_name`: Name of the service.
* `level`: Log severity level, optional.
* `keyword`: Search term, optional.
* `limit`: Maximum number of results.

Expected response:

* Matching logs, including timestamp, severity level, service, and message.

### `get_api_errors`

**Purpose:** Retrieve recorded API errors.

Parameters:

* `service_name`: Name of the service.
* `limit`: Maximum number of results.

Expected response:

* Matching errors, available HTTP status codes, and related information.

### `get_service_metrics`

**Purpose:** Retrieve simulated operational metrics.

Parameters:

* `service_name`: Name of the service.
* `metric_name`: Name of the metric, optional.

Expected response:

* Available metrics and their corresponding values.

### `get_database_status`

**Purpose:** Retrieve the simulated status of the database associated with an application.

Parameters:

* `service_name`: Name of the service, when applicable.

Expected response:

* Recorded database status.
* Available connectivity and capacity information.

### `get_database_errors`

**Purpose:** Search for database-related errors.

Parameters:

* `service_name`: Name of the service, optional.
* `limit`: Maximum number of results.

Expected response:

* Matching errors, including timeouts and connection issues when present.

### `get_recent_deployments`

**Purpose:** Retrieve recent deployments.

Parameters:

* `service_name`: Name of the service.
* `limit`: Maximum number of results.

Expected response:

* Deployed version.
* Deployment timestamp.
* Available deployment outcome information.

### `get_deployment_details`

**Purpose:** Retrieve details about a specific deployment.

Parameters:

* `deployment_id`: Deployment identifier.

Expected response:

* Deployment identifier, version, timestamp, and other available details.

## 4. MCP Layer Responsibilities

The MCP layer must:

1. Expose the available tools to agents.
2. Validate input parameters.
3. Execute authorized queries.
4. Return structured results.
5. Handle errors and invalid inputs.
6. Prevent write operations and data modifications.

The implementation may use Python functions for database queries and an MCP server to expose them.

## 5. Tool Usage Rules

* Agents should select tools relevant to their assigned tasks.
* Independent queries may execute in parallel.
* Empty results must be treated as missing evidence, not proof that the system is healthy.
* Query failures must be distinguished from successful queries with no results.
* Result limits must be enforced.
* User-provided input must not be directly concatenated into SQL statements.

## 6. Limitations

Tools access only simulated project data.

The following operations are prohibited:

* Accessing real infrastructure.
* Executing arbitrary operating system commands.
* Modifying services or deployments.
* Restarting services automatically.
* Modifying or deleting database records.
* Executing production remediation actions.
