"""
Deployment Agent for analyzing recent deployments and correlations with incidents.
"""

from typing import Any

from src.agents.base_agent import BaseAgent
from src.mcp import get_recent_deployments, search_logs


class DeploymentAgent(BaseAgent):
    """
    Analyzes recent deployments and determines whether an incident may be correlated with a deployment.
    """

    def __init__(self, require_api_key: bool = True):
        """
        Initialize the Deployment Agent.

        Args:
            require_api_key: If True, validates that API key is configured.
        """
        super().__init__("deployment_agent.md", require_api_key=require_api_key)

    def investigate(self, service_name: str, context: str) -> str:
        """
        Investigate deployment-related issues.

        Args:
            service_name: Name of the service to investigate.
            context: Additional context about the incident.

        Returns:
            Investigation results as string.
        """
        # Gather deployment data
        deployments = get_recent_deployments(service_name, limit=5)
        deployment_logs = search_logs(service_name, keyword="deployment", limit=20)

        # Build user message with context and data
        user_message = f"""
Incident Context:
{context}

Recent Deployments:
{deployments}

Deployment-Related Logs:
{deployment_logs}

Analyze the deployment data to determine whether this incident may be correlated with a recent deployment.
"""

        return self.invoke(user_message)
