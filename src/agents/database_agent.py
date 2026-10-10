"""
Database Agent for investigating database-related problems.
"""

from typing import Any

from src.agents.base_agent import BaseAgent
from src.mcp import get_database_status, get_database_errors, get_service_metrics


class DatabaseAgent(BaseAgent):
    """
    Investigates database-related problems, including connection issues, performance problems, and error patterns.
    """

    def __init__(self, require_api_key: bool = True):
        """
        Initialize the Database Agent.

        Args:
            require_api_key: If True, validates that API key is configured.
        """
        super().__init__("database_agent.md", require_api_key=require_api_key)

    def investigate(self, service_name: str, context: str) -> str:
        """
        Investigate database-related issues.

        Args:
            service_name: Name of the service to investigate.
            context: Additional context about the incident.

        Returns:
            Investigation results as string.
        """
        # Gather database data
        database_status = get_database_status(service_name)
        database_errors = get_database_errors(service_name, limit=20)
        metrics = get_service_metrics(service_name)

        # Build user message with context and data
        user_message = f"""
Incident Context:
{context}

Database Status:
{database_status}

Recent Database Errors:
{database_errors}

Database Metrics:
{metrics}

Analyze the database data to identify connection issues, performance problems, and error patterns.
"""

        return self.invoke(user_message)
