"""
MCP Server for exposing operational data tools.

This server provides read-only access to simulated operational data.
"""

import asyncio
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from src.mcp.tools import (
    get_api_errors,
    get_database_errors,
    get_database_status,
    get_deployment_details,
    get_recent_deployments,
    get_service_metrics,
    get_service_status,
    search_logs,
)

# Create MCP server
server = Server("incident-analyzer-mcp")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """
    List available MCP tools.

    Returns:
        List of available tools.
    """
    return [
        Tool(
            name="get_service_status",
            description="Retrieve the current status of a service",
            inputSchema={
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Name of the service",
                    }
                },
                "required": ["service_name"],
            },
        ),
        Tool(
            name="search_logs",
            description="Search logs associated with a service",
            inputSchema={
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Name of the service",
                    },
                    "level": {
                        "type": "string",
                        "description": "Log severity level (optional)",
                    },
                    "keyword": {
                        "type": "string",
                        "description": "Search term in message (optional)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 50)",
                    },
                },
                "required": ["service_name"],
            },
        ),
        Tool(
            name="get_api_errors",
            description="Retrieve recorded API errors",
            inputSchema={
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Name of the service",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 50)",
                    },
                },
                "required": ["service_name"],
            },
        ),
        Tool(
            name="get_service_metrics",
            description="Retrieve simulated operational metrics",
            inputSchema={
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Name of the service",
                    },
                    "metric_name": {
                        "type": "string",
                        "description": "Name of the metric (optional)",
                    },
                },
                "required": ["service_name"],
            },
        ),
        Tool(
            name="get_database_status",
            description="Retrieve the simulated status of the database",
            inputSchema={
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Name of the service (optional)",
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="get_database_errors",
            description="Search for database-related errors",
            inputSchema={
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Name of the service (optional)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 50)",
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="get_recent_deployments",
            description="Retrieve recent deployments",
            inputSchema={
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Name of the service",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 10)",
                    },
                },
                "required": ["service_name"],
            },
        ),
        Tool(
            name="get_deployment_details",
            description="Retrieve details about a specific deployment",
            inputSchema={
                "type": "object",
                "properties": {
                    "deployment_id": {
                        "type": "integer",
                        "description": "Deployment identifier",
                    },
                },
                "required": ["deployment_id"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """
    Execute an MCP tool.

    Args:
        name: Tool name.
        arguments: Tool arguments.

    Returns:
        Tool result as text content.
    """
    try:
        if name == "get_service_status":
            result = get_service_status(**arguments)
        elif name == "search_logs":
            result = search_logs(**arguments)
        elif name == "get_api_errors":
            result = get_api_errors(**arguments)
        elif name == "get_service_metrics":
            result = get_service_metrics(**arguments)
        elif name == "get_database_status":
            result = get_database_status(**arguments)
        elif name == "get_database_errors":
            result = get_database_errors(**arguments)
        elif name == "get_recent_deployments":
            result = get_recent_deployments(**arguments)
        elif name == "get_deployment_details":
            result = get_deployment_details(**arguments)
        else:
            result = {"error": f"Unknown tool: {name}"}

        import json
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        import json
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, indent=2))]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
