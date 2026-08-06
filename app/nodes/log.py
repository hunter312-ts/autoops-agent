from langgraph.runtime import Runtime

from app.core.logging import logger
from app.graph.context import RuntimeContext
from app.graph.state import AgentState


def log_node(
    state: AgentState,
    runtime: Runtime[RuntimeContext],
) -> AgentState:
    """
    Log the final outcome of the workflow
    and persist it to SQLite.
    """

    request = state.get("request")
    classification = state.get("classification")

    logger.info("=" * 60)
    logger.info("WORKFLOW COMPLETED")

    if request:
        logger.info(f"Request ID : {request.request_id}")
        logger.info(f"Source     : {request.source}")
        logger.info(f"Sender     : {request.sender}")

    if classification:
        logger.info(f"Intent     : {classification.intent}")
        logger.info(f"Confidence : {classification.confidence}")
        logger.info(f"Risk       : {classification.risk}")

    logger.info(f"Route      : {state.get('route')}")
    logger.info(f"Approval   : {state.get('approval')}")
    logger.info(f"Execution  : {state.get('execution_result')}")
    logger.info(f"Error      : {state.get('error')}")

    # -----------------------------------------
    # Save workflow to SQLite
    # -----------------------------------------

    runtime.context.services.sqlite.save_workflow(state)

    logger.info("Workflow saved to SQLite.")

    logger.info("=" * 60)

    return state