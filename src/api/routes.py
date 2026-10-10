"""
FastAPI routes for incident analysis.
"""

from fastapi import APIRouter

from src.api.models import ChatRequest, ChatResponse
from src.orchestrator import IncidentOrchestrator

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Process an incident analysis request.

    Args:
        request: Chat request with user message.

    Returns:
        Chat response with analysis and execution trace.
    """
    orchestrator = IncidentOrchestrator(require_api_key=True)
    result = orchestrator.invoke(request.message)

    return ChatResponse(
        response=result.final_response or "No response generated",
        execution_trace=result.execution_trace,
    )
