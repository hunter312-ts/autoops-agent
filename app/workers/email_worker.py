"""
email_worker.py

Polls Gmail for unread emails and processes them through
the AutoOps LangGraph workflow.
"""

from uuid import uuid4

from app.config.runtime import RuntimeConfig
from app.graph.context import RuntimeContext
from app.graph.graph import graph
from app.services.container import ServiceContainer
from app.core.logging import logger


def process_emails(runtime_config: RuntimeConfig) -> None:
    """
    Fetch unread emails and process them through the workflow.
    """

    logger.info("Starting Email Worker...")

    # -----------------------------------------
    # Initialize runtime services
    # -----------------------------------------

    services = ServiceContainer(runtime_config)

    runtime_context = RuntimeContext(
        services=services,
    )

    # -----------------------------------------
    # Authenticate Gmail
    # -----------------------------------------

    services.gmail.authenticate()

    emails = services.gmail.fetch_unread_emails()

    logger.info(f"Found {len(emails)} unread emails.")

    # -----------------------------------------
    # Process each email
    # -----------------------------------------

    for email in emails:

        thread_id = f"THREAD-{uuid4().hex}"

        try:

            logger.info("-" * 60)
            logger.info(f"Processing: {email['subject']}")

            raw_request = services.gmail.convert_to_raw_request(
                email
            )

            state = {
                "thread_id": thread_id,
                "raw_request": raw_request,
                "request": None,
                "classification": None,
                "route": None,
                "approval": None,
                "execution_result": None,
                "error": None,
            }

            result = graph.invoke(
                state,
                context=runtime_context,
                config={
                    "configurable": {
                        "thread_id": thread_id
                    }
                },
            )

            # Mark email as processed only if there
            # wasn't an interrupt or an error.
            if (
                "__interrupt__" not in result
                and result["error"] is None
            ):
                services.gmail.mark_as_processed(
                    email["id"]
                )

        except Exception:

            logger.exception(
                f"Failed processing email {email['id']}"
            )

    logger.info("Email Worker finished.")