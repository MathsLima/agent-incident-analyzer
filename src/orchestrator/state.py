"""
Shared state for LangGraph workflow.

Defines the state exchanged between agents during incident investigation.
"""

from typing import Any, Optional

from pydantic import BaseModel, Field


class IncidentState(BaseModel):
    """
    Shared state for the incident investigation workflow.

    This state is passed between LangGraph nodes and contains all information
    collected during the investigation.
    """

    # User input
    user_request: str = Field(description="The original user request describing the incident")

    # Incident classification
    incident_type: Optional[str] = Field(default=None, description="Type of incident (API, database, deployment, etc.)")

    # Agent selection
    selected_agents: list[str] = Field(default_factory=list, description="List of selected investigation agents")

    # Evidence collected by investigation agents
    logs_evidence: Optional[str] = Field(default=None, description="Evidence from Log Agent")
    api_evidence: Optional[str] = Field(default=None, description="Evidence from API Agent")
    database_evidence: Optional[str] = Field(default=None, description="Evidence from Database Agent")
    deployment_evidence: Optional[str] = Field(default=None, description="Evidence from Deployment Agent")

    # Root cause analysis
    root_cause: Optional[str] = Field(default=None, description="Probable root cause determined by Root Cause Agent")
    confidence: Optional[str] = Field(default=None, description="Confidence level in root cause determination")

    # Recommended actions
    recommended_actions: Optional[str] = Field(default=None, description="Recommended actions from Action Agent")

    # Execution trace
    execution_trace: list[str] = Field(default_factory=list, description="Trace of executed steps")

    # Final response
    final_response: Optional[str] = Field(default=None, description="Final response to the user")

    # Service name (extracted from request)
    service_name: Optional[str] = Field(default=None, description="Name of the affected service")

    def add_trace(self, message: str) -> None:
        """
        Add a message to the execution trace.

        Args:
            message: Trace message to add.
        """
        self.execution_trace.append(message)

    def get_all_evidence(self) -> dict[str, Any]:
        """
        Get all collected evidence as a dictionary.

        Returns:
            Dictionary containing all evidence fields.
        """
        evidence = {}
        if self.logs_evidence:
            evidence["logs"] = self.logs_evidence
        if self.api_evidence:
            evidence["api"] = self.api_evidence
        if self.database_evidence:
            evidence["database"] = self.database_evidence
        if self.deployment_evidence:
            evidence["deployment"] = self.deployment_evidence
        return evidence
