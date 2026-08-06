from app.core.logging import logger
from app.graph.state import AgentState


def router(state: AgentState) -> AgentState:
    """
    Decide the next workflow step based on the
    classification result.
    """

    classification = state["classification"]

    if classification is None:
        logger.error("No classification found.")
        state["error"] = "Classification missing."
        return state

    logger.info("Running Router...")

    # Rule 1: Low confidence
    if classification.confidence < 0.75:
        state["route"] = "HUMAN_APPROVAL"

    # Rule 2: High-risk requests
    elif classification.risk == "HIGH":
        state["route"] = "HUMAN_APPROVAL"

    # Rule 3: Refunds & Account Issues
    elif classification.intent in [
        "Refund Request",
        "Account Issue",
    ]:
        state["route"] = "HUMAN_APPROVAL"

    # Rule 4: Create ticket
    elif classification.intent in [
        "Complaint",
        "Feature Request",
        "Bug Report",
    ]:
        state["route"] = "CREATE_TICKET"

    # Rule 5: Auto reply
    else:
        state["route"] = "AUTO_REPLY"

    logger.info(f"Next Route: {state['route']}")

    return state

def route_decision(state: AgentState) -> str:
    """
    Return the next node name based on
    the route stored in AgentState.
    """

    return state["route"]