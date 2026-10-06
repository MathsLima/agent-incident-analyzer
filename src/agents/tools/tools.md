# System Tools

This document describes the operational tools available to the Agent Incident Analyzer.

## MCP Tools

All operational data access must go through MCP.

### get_recent_logs

Returns recent logs for a service.

Input:

```text
service_name
limit
```

Expected use:

* Investigate recent application errors.
* Identify error patterns.
* Correlate incidents with deployments.

### search_logs

Searches logs using a text query.

Input:

```text
query
service_name (optional)
limit
```

Expected use:

* Search for specific errors.
* Find stack traces or recurring messages.

### get_service_status

Returns the current simulated status of a service.

Input:

```text
service_name
```

Expected use:

* Determine whether a service is healthy, degraded, or unavailable.

### get_api_errors

Returns simulated API errors for a service.

Input:

```text
service_name
limit
```

Expected use:

* Analyze HTTP errors.
* Identify error patterns.

### get_service_metrics

Returns simulated metrics.

Input:

```text
service_name
```

Expected use:

* Analyze latency.
* Analyze error rate.
* Identify abnormal behavior.

### get_database_status

Returns simulated database status.

Input:

```text
database_name
```

Expected use:

* Determine whether database health could explain an incident.

### get_database_errors

Returns simulated database errors.

Input:

```text
database_name
limit
```

Expected use:

* Identify database-related failures.

### get_recent_deployments

Returns recent deployments.

Input:

```text
service_name
limit
```

Expected use:

* Correlate incidents with recent releases.

### get_deployment_details

Returns details about a deployment.

Input:

```text
deployment_id
```

Expected use:

* Investigate version changes.
* Correlate deployment timing with incident onset.

## Safety

MCP tools in this educational project are read-only.

They must not:

* Restart services.
* Modify databases.
* Deploy code.
* Execute shell commands.
* Change infrastructure.
* Delete data.

If a future tool requires mutation, it must be explicitly documented and approved before implementation.