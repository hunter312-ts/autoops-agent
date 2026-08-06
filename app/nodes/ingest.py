from uuid import uuid4

from app.core.logging import logger
from app.graph.state import AgentState
from app.models.schemas import SupportRequest


def ingest_request(state: AgentState) -> AgentState:
    """
    Convert a raw incoming request into a SupportRequest.
    """

    logger.info("Starting request ingestion...")

    raw_request = state["raw_request"]

    if raw_request is None:
        return {
            **state,
            "error": "Raw request is missing.",
        }

    try:
        required_fields = ["source", "sender", "body"]

        for field in required_fields:
            if field not in raw_request:
                raise ValueError(f"Missing required field: {field}")

        request = SupportRequest(
            request_id=f"REQ-{uuid4().hex[:8].upper()}",
            source=raw_request["source"],
            sender=raw_request["sender"],
            subject=raw_request.get("subject", ""),
            body=raw_request["body"],
        )

        logger.info(
            f"Request {request.request_id} successfully ingested "
            f"from {request.source}."
        )

        return {
            **state,
            "request": request,
        }

    except Exception:
        logger.exception("Ingestion failed.")

        return {
            **state,
            "error": "Failed to ingest request.",
        }