from langgraph.types import interrupt

from app.core.logging import logger
from app.graph.state import AgentState


def approve_node(state: AgentState):
    logger.info("Waiting for human approval...")

    decision = interrupt(
        {
            "request_id": state["request"].request_id,
            "sender": state["request"].sender,
            "subject": state["request"].subject,
            "intent": state["classification"].intent,
            "risk": state["classification"].risk,
            "reason": state["classification"].reason,
        }
    )

    logger.info(f"Human decision received: {decision}")

    return {
        "approval": decision,
    }