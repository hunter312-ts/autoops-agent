from langgraph.runtime import Runtime

from app.core.logging import logger
from app.graph.context import RuntimeContext
from app.graph.state import AgentState


def classify_node(
    state: AgentState,
    runtime: Runtime[RuntimeContext],
) -> AgentState:
    """
    LangGraph node responsible for classifying
    a customer support request.
    """

    logger.info("Starting Classification Node...")

    try:
        logger.info(runtime.context.services.groq)
        logger.info(state["request"])
        classification = runtime.context.services.groq.classify(
            state["request"]
        )

        state["classification"] = classification

        logger.info(
            f"Intent: {classification.intent} | "
            f"Confidence: {classification.confidence}"
        )

    except Exception as e:

        logger.exception("Classification failed.")

        state["error"] = str(e)

    return state