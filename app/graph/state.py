from typing import Optional
from typing_extensions import TypedDict

from app.models.schemas import (
    SupportRequest,
    ClassificationResult,
)


class AgentState(TypedDict):
    """
    Shared state passed between LangGraph nodes.
    """
    thread_id: Optional[str]
    # Raw input from Gmail/Webhook/Slack
    raw_request: Optional[dict]

    # Standardized request after Ingest Node
    request: Optional[SupportRequest]

    # AI classification
    classification: Optional[ClassificationResult]

    # Next workflow route
    route: Optional[str]

    # Human approval decision
    approval: Optional[str]

    # Execution result
    execution_result: Optional[str]

    # Error message
    error: Optional[str]

    generated_reply: Optional[str]