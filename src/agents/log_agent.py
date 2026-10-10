"""
Log Agent for analyzing application and infrastructure logs.
"""

from typing import Any

from src.agents.base_agent import BaseAgent
from src.mcp import search_logs, get_service_status


class LogAgent(BaseAgent):
    """
    Analyzes application and infrastructure logs to identify relevant errors, patterns, and timestamps.
    """

    def __init__(self, require_api_key: bool = True):
        """
        Initialize the Log Agent.

        Args:
            require_api_key: If True, validates that API key is configured.
        """
        super().__init__("log_agent.md", require_api_key=require_api_key)

    def investigate(self, service_name: str, context: str) -> str:
        """
        Investigate logs for a service.

        Args:
            service_name: Name of the service to investigate.
            context: Additional context about the incident.

        Returns:
            Investigation results as string.
        """
        # Gather log data
        service_status = get_service_status(service_name)
        error_logs = search_logs(service_name, level="ERROR", limit=20)
        warn_logs = search_logs(service_name, level="WARN", limit=20)

        # Build user message with context and data
        user_message = f"""
Incident Context:
{context}

Service Status:
{service_status}

Recent Error Logs:
{error_logs}

Recent Warning Logs:
{warn_logs}

Analyze the logs and identify relevant errors, patterns, and timestamps related to this incident.
"""

        return self.invoke(user_message)
