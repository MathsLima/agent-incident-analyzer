"""
Root Cause Agent for analyzing collected evidence and determining probable root cause.
"""

from typing import Any

from src.agents.base_agent import BaseAgent


class RootCauseAgent(BaseAgent):
    """
    Analyzes the evidence collected by investigation agents and determines the most probable root cause.
    """

    def __init__(self, require_api_key: bool = True):
        """
        Initialize the Root Cause Agent.

        Args:
            require_api_key: If True, validates that API key is configured.
        """
        super().__init__("root_cause_agent.md", require_api_key=require_api_key)

    def analyze(self, evidence: dict[str, Any]) -> str:
        """
        Analyze collected evidence to determine probable root cause.

        Args:
            evidence: Dictionary containing evidence from investigation agents.

        Returns:
            Root cause analysis as string.
        """
        # Build user message with evidence
        user_message = f"""
Collected Evidence:

{evidence}

Analyze this evidence and determine the most probable root cause of the incident.
"""

        return self.invoke(user_message)
