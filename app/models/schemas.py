from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field


class SupportRequest(BaseModel):
   """
    Standard request object used throughout the AutoOps Agent.
    Every incoming request (Gmail, Webhook, Slack, etc.)
    is converted into this format before entering LangGraph.
    """
   request_id: str = Field( ..., description="Unique request identifier.")
   source: Literal["gmail", "webhook", "slack"] = Field( ...,description="Origin of the request.")
   sender: str = Field(...,description="Email address or user who sent the request.")
   subject: str = Field(default="",description="Subject or title of the request.")
   body: str = Field(...,description="Main message content.")
   received_at: datetime = Field(default_factory=datetime.now,description="Timestamp when the request was received.")
   status: str = Field(default="NEW",description="Current processing status.")


class ClassificationResult(BaseModel):
    """
    Output of the Classification Node.
    Represents the AI's understanding of the customer's request.
    """
    intent: Literal["Complaint","Feature Request","Bug Report","Refund Request","Billing Question","Technical Support",
    "Account Issue","General Inquiry",] = Field(...,description="Detected customer intent.")
    confidence: float = Field(...,ge=0.0,le=1.0,description="Confidence score returned by the LLM.")
    risk:Literal["LOW","MEDIUM","HIGH"] = Field(...,description="Automation risk level.")
    priority: Literal["LOW","MEDIUM","HIGH","CRITICAL"] = Field(...,description="Business priority of the request.")
    reason: str = Field(...,description="Explanation for the classification.")