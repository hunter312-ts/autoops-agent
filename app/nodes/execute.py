from langgraph.runtime import Runtime

from app.graph.context import RuntimeContext

from app.core.logging import logger
from app.graph.state import AgentState

#---------------- Execute Node ----------------

def execute_node(
    state: AgentState,
    runtime: Runtime[RuntimeContext],
) -> AgentState:
    """
    Execute the action selected by the Router.

    Handles:
    - AUTO_REPLY
    - CREATE_TICKET
    - HUMAN_APPROVAL
    """

    logger.info("Execute Node started.")

    route = state["route"]
    request = state["request"]
    try:

        # ---------------- AUTO REPLY ----------------

        if route == "AUTO_REPLY":

            gmail = runtime.context.services.gmail

            if gmail.service is None:
                gmail.authenticate()
            gmail.send_reply(
                to_email=request.sender,
                subject=request.subject,
                body="""
        Hello,

        Thank you for contacting us.

        We have received your request.

        Our support team will contact you shortly.

        Best regards,
        AutoOps AI
        """,
            )
        # Mark the original email as read
        if "id" in state["raw_request"]:
            gmail.mark_as_processed(
                state["raw_request"]["id"]
            )

            result = "Email reply sent successfully."

        # ---------------- CREATE TICKET ----------------

        elif route == "CREATE_TICKET":

            result = simulate_create_ticket()

        # ---------------- HUMAN APPROVAL ----------------

        elif route == "HUMAN_APPROVAL":

            if state["approval"]:

                logger.info("Human approved the request.")

                result = simulate_refund()

            else:

                logger.info("Human rejected the request.")

                result = "Refund request rejected."

        # ---------------- UNKNOWN ----------------

        else:

            result = f"No execution required for route: {route}"

        logger.info(result)

        return {
    "execution_result": result,
}

    except Exception as e:

        logger.exception("Execution failed.")

        return {
    "error": str(e),
}


def simulate_create_ticket():

    logger.info("Simulating ticket creation...")

    return "Support ticket created successfully."


def simulate_refund():

    logger.info("Simulating refund...")

    return "Refund processed successfully."