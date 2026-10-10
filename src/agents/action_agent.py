"""
Action Agent for generating recommended actions based on identified root cause.
"""

from typing import Any

from src.agents.base_agent import BaseAgent


class ActionAgent(BaseAgent):
    """
    Generates recommended actions to investigate, mitigate, or resolve an incident based on the identified root cause.
    """

    def __init__(self, require_api_key: bool = True):
        """
        Initialize the Action Agent.

        Args:
            require_api_key: If True, validates that API key is configured.
        """
        super().__init__("action_agent.md", require_api_key=require_api_key)

    def recommend(self, root_cause_analysis: str) -> str:
        """
        Generate recommended actions based on root cause analysis.

        Args:
            root_cause_analysis: Root cause analysis from the Root Cause Agent.

        Returns:
            Recommended actions as string.
        """
        # Build user message with root cause analysis
        user_message = f"""
Root Cause Analysis:

{root_cause_analysis}

Generate recommended actions to investigate, mitigate, or resolve this incident.
Remember to provide recommendations only, not execution instructions.
"""

        return self.invoke(user_message)
