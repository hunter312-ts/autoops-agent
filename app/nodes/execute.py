from app.core.logging import logger
from app.graph.state import AgentState

#---------------- Execute Node ----------------

def execute_node(state: AgentState) -> AgentState:
    """
    Execute the action selected by the Router.

    Handles:
    - AUTO_REPLY
    - CREATE_TICKET
    - HUMAN_APPROVAL
    """

    logger.info("Execute Node started.")

    route = state["route"]

    try:

        # ---------------- AUTO REPLY ----------------

        if route == "AUTO_REPLY":

            result = simulate_auto_reply()

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


def simulate_auto_reply():

    logger.info("Simulating email reply...")

    return "Email reply sent successfully."


def simulate_create_ticket():

    logger.info("Simulating ticket creation...")

    return "Support ticket created successfully."


def simulate_refund():

    logger.info("Simulating refund...")

    return "Refund processed successfully."