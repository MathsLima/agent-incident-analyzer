"""
API Agent for analyzing API and service information.
"""

from typing import Any

from src.agents.base_agent import BaseAgent
from src.mcp import get_service_status, get_api_errors, get_service_metrics


class APIAgent(BaseAgent):
    """
    Analyzes API and service information to understand service health, error patterns, and performance metrics.
    """

    def __init__(self, require_api_key: bool = True):
        """
        Initialize the API Agent.

        Args:
            require_api_key: If True, validates that API key is configured.
        """
        super().__init__("api_agent.md", require_api_key=require_api_key)

    def investigate(self, service_name: str, context: str) -> str:
        """
        Investigate API and service information.

        Args:
            service_name: Name of the service to investigate.
            context: Additional context about the incident.

        Returns:
            Investigation results as string.
        """
        # Gather API data
        service_status = get_service_status(service_name)
        api_errors = get_api_errors(service_name, limit=20)
        metrics = get_service_metrics(service_name)

        # Build user message with context and data
        user_message = f"""
Incident Context:
{context}

Service Status:
{service_status}

Recent API Errors:
{api_errors}

Service Metrics:
{metrics}

Analyze the API and service data to understand service health, error patterns, and performance issues.
"""

        return self.invoke(user_message)
