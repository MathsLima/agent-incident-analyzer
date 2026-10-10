"""
LangGraph workflow for incident investigation orchestration.
"""

from typing import Any

from langgraph.graph import StateGraph, END

from src.agents import (
    ActionAgent,
    APIAgent,
    DatabaseAgent,
    DeploymentAgent,
    LogAgent,
    RootCauseAgent,
)
from src.llm import get_llm
from src.orchestrator.state import IncidentState


class IncidentOrchestrator:
    """
    Orchestrates the incident investigation workflow using LangGraph.
    """

    def __init__(self, require_api_key: bool = True):
        """
        Initialize the orchestrator.

        Args:
            require_api_key: If True, validates that API key is configured.
        """
        self.require_api_key = require_api_key
        self.llm = get_llm(require_api_key=require_api_key)

        # Initialize agents
        self.log_agent = LogAgent(require_api_key=require_api_key)
        self.api_agent = APIAgent(require_api_key=require_api_key)
        self.database_agent = DatabaseAgent(require_api_key=require_api_key)
        self.deployment_agent = DeploymentAgent(require_api_key=require_api_key)
        self.root_cause_agent = RootCauseAgent(require_api_key=require_api_key)
        self.action_agent = ActionAgent(require_api_key=require_api_key)

        # Build the graph
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """
        Build the LangGraph workflow.

        Returns:
            Compiled StateGraph.
        """
        workflow = StateGraph(IncidentState)

        # Add nodes
        workflow.add_node("orchestrator", self._orchestrator_node)
        workflow.add_node("log_agent", self._log_agent_node)
        workflow.add_node("api_agent", self._api_agent_node)
        workflow.add_node("database_agent", self._database_agent_node)
        workflow.add_node("deployment_agent", self._deployment_agent_node)
        workflow.add_node("root_cause_agent", self._root_cause_agent_node)
        workflow.add_node("action_agent", self._action_agent_node)
        workflow.add_node("final_response", self._final_response_node)

        # Set entry point
        workflow.set_entry_point("orchestrator")

        # Add conditional edges from orchestrator
        workflow.add_conditional_edges(
            "orchestrator",
            self._route_agents,
            {
                "log_agent": "log_agent",
                "api_agent": "api_agent",
                "database_agent": "database_agent",
                "deployment_agent": "deployment_agent",
                "root_cause": "root_cause_agent",
            },
        )

        # Add edges from investigation agents to root cause
        workflow.add_edge("log_agent", "root_cause_agent")
        workflow.add_edge("api_agent", "root_cause_agent")
        workflow.add_edge("database_agent", "root_cause_agent")
        workflow.add_edge("deployment_agent", "root_cause_agent")

        # Add edge from root cause to action
        workflow.add_edge("root_cause_agent", "action_agent")

        # Add edge from action to final response
        workflow.add_edge("action_agent", "final_response")

        # Add edge from final response to end
        workflow.add_edge("final_response", END)

        return workflow.compile()

    def _orchestrator_node(self, state: IncidentState) -> IncidentState:
        """
        Orchestrator node: Classify incident and select agents.

        Args:
            state: Current incident state.

        Returns:
            Updated incident state.
        """
        state.add_trace("[ORCHESTRATOR] Incident received")

        # Simple agent selection based on keywords in the request
        request_lower = state.user_request.lower()

        selected_agents = []

        if "log" in request_lower or "error" in request_lower:
            selected_agents.append("log_agent")

        if "api" in request_lower or "http" in request_lower or "500" in request_lower:
            selected_agents.append("api_agent")

        if "database" in request_lower or "db" in request_lower or "timeout" in request_lower:
            selected_agents.append("database_agent")

        if "deployment" in request_lower or "deploy" in request_lower or "version" in request_lower:
            selected_agents.append("deployment_agent")

        # Default to API agent if no specific keywords found
        if not selected_agents:
            selected_agents.append("api_agent")

        state.selected_agents = selected_agents
        state.incident_type = self._classify_incident(request_lower)

        # Extract service name (simple heuristic)
        state.service_name = self._extract_service_name(state.user_request)

        state.add_trace(f"[ORCHESTRATOR] Selected agents: {', '.join(selected_agents)}")

        return state

    def _route_agents(self, state: IncidentState) -> str:
        """
        Route to the appropriate investigation agent.

        Args:
            state: Current incident state.

        Returns:
            Next node name.
        """
        # For simplicity, route to the first selected agent
        # In a more complex implementation, this could execute agents in parallel
        if state.selected_agents:
            return state.selected_agents[0]
        return "api_agent"

    def _log_agent_node(self, state: IncidentState) -> IncidentState:
        """
        Log Agent node: Analyze logs.

        Args:
            state: Current incident state.

        Returns:
            Updated incident state.
        """
        state.add_trace("[LOG_AGENT] Started")

        service_name = state.service_name or "unknown"
        context = f"Incident: {state.user_request}"

        try:
            state.logs_evidence = self.log_agent.investigate(service_name, context)
            state.add_trace("[LOG_AGENT] Completed")
        except Exception as e:
            state.logs_evidence = f"Error: {str(e)}"
            state.add_trace(f"[LOG_AGENT] Failed: {str(e)}")

        return state

    def _api_agent_node(self, state: IncidentState) -> IncidentState:
        """
        API Agent node: Analyze API information.

        Args:
            state: Current incident state.

        Returns:
            Updated incident state.
        """
        state.add_trace("[API_AGENT] Started")

        service_name = state.service_name or "unknown"
        context = f"Incident: {state.user_request}"

        try:
            state.api_evidence = self.api_agent.investigate(service_name, context)
            state.add_trace("[API_AGENT] Completed")
        except Exception as e:
            state.api_evidence = f"Error: {str(e)}"
            state.add_trace(f"[API_AGENT] Failed: {str(e)}")

        return state

    def _database_agent_node(self, state: IncidentState) -> IncidentState:
        """
        Database Agent node: Analyze database information.

        Args:
            state: Current incident state.

        Returns:
            Updated incident state.
        """
        state.add_trace("[DATABASE_AGENT] Started")

        service_name = state.service_name or "unknown"
        context = f"Incident: {state.user_request}"

        try:
            state.database_evidence = self.database_agent.investigate(service_name, context)
            state.add_trace("[DATABASE_AGENT] Completed")
        except Exception as e:
            state.database_evidence = f"Error: {str(e)}"
            state.add_trace(f"[DATABASE_AGENT] Failed: {str(e)}")

        return state

    def _deployment_agent_node(self, state: IncidentState) -> IncidentState:
        """
        Deployment Agent node: Analyze deployment information.

        Args:
            state: Current incident state.

        Returns:
            Updated incident state.
        """
        state.add_trace("[DEPLOYMENT_AGENT] Started")

        service_name = state.service_name or "unknown"
        context = f"Incident: {state.user_request}"

        try:
            state.deployment_evidence = self.deployment_agent.investigate(service_name, context)
            state.add_trace("[DEPLOYMENT_AGENT] Completed")
        except Exception as e:
            state.deployment_evidence = f"Error: {str(e)}"
            state.add_trace(f"[DEPLOYMENT_AGENT] Failed: {str(e)}")

        return state

    def _root_cause_agent_node(self, state: IncidentState) -> IncidentState:
        """
        Root Cause Agent node: Analyze evidence and determine root cause.

        Args:
            state: Current incident state.

        Returns:
            Updated incident state.
        """
        state.add_trace("[ROOT_CAUSE_AGENT] Started")

        evidence = state.get_all_evidence()

        try:
            state.root_cause = self.root_cause_agent.analyze(evidence)
            state.confidence = "medium"  # Simplified for demo
            state.add_trace("[ROOT_CAUSE_AGENT] Completed")
        except Exception as e:
            state.root_cause = f"Error: {str(e)}"
            state.confidence = "low"
            state.add_trace(f"[ROOT_CAUSE_AGENT] Failed: {str(e)}")

        return state

    def _action_agent_node(self, state: IncidentState) -> IncidentState:
        """
        Action Agent node: Generate recommended actions.

        Args:
            state: Current incident state.

        Returns:
            Updated incident state.
        """
        state.add_trace("[ACTION_AGENT] Started")

        try:
            state.recommended_actions = self.action_agent.recommend(state.root_cause or "")
            state.add_trace("[ACTION_AGENT] Completed")
        except Exception as e:
            state.recommended_actions = f"Error: {str(e)}"
            state.add_trace(f"[ACTION_AGENT] Failed: {str(e)}")

        return state

    def _final_response_node(self, state: IncidentState) -> IncidentState:
        """
        Final response node: Generate final response for user.

        Args:
            state: Current incident state.

        Returns:
            Updated incident state.
        """
        state.add_trace("[ORCHESTRATOR] Final response generated")

        # Build final response
        response_parts = [
            f"## Incident Analysis\n\n",
            f"**Request:** {state.user_request}\n\n",
            f"**Selected Agents:** {', '.join(state.selected_agents)}\n\n",
        ]

        if state.root_cause:
            response_parts.append(f"**Probable Root Cause:**\n{state.root_cause}\n\n")

        if state.recommended_actions:
            response_parts.append(f"**Recommended Actions:**\n{state.recommended_actions}\n\n")

        response_parts.append(f"**Execution Trace:**\n")
        for trace in state.execution_trace:
            response_parts.append(f"- {trace}\n")

        state.final_response = "".join(response_parts)

        return state

    def _classify_incident(self, request: str) -> str:
        """
        Classify the incident type based on the request.

        Args:
            request: User request.

        Returns:
            Incident type string.
        """
        request_lower = request.lower()

        if "database" in request_lower or "db" in request_lower:
            return "database"
        elif "deployment" in request_lower or "deploy" in request_lower:
            return "deployment"
        elif "api" in request_lower or "http" in request_lower:
            return "api"
        else:
            return "general"

    def _extract_service_name(self, request: str) -> str:
        """
        Extract service name from the request.

        Args:
            request: User request.

        Returns:
            Service name or None.
        """
        # Simple heuristic: look for common service names
        request_lower = request.lower()

        if "payments" in request_lower:
            return "payments-api"
        elif "user" in request_lower:
            return "user-service"
        elif "database" in request_lower or "db" in request_lower:
            return "main-database"
        else:
            return "payments-api"  # Default for demo

    def invoke(self, user_request: str) -> IncidentState:
        """
        Invoke the orchestrator with a user request.

        Args:
            user_request: User's incident description.

        Returns:
            Final incident state with analysis results.
        """
        initial_state = IncidentState(user_request=user_request)
        final_state = self.graph.invoke(initial_state)
        return final_state
