from uuid import uuid4

import streamlit as st

from app.graph.graph import graph


def show_inbox_page():
    """
    Inbox page.

    Displays unread Gmail messages and allows
    the user to process them.
    """

    st.header("📬 Inbox")

    # --------------------------------------------------
    # Check Configuration
    # --------------------------------------------------

    if st.session_state.runtime_config is None:

        st.warning("Please configure AutoOps first.")

        return

    if not st.session_state.get("authenticated", False):

        st.warning("Please authenticate Gmail first.")

        return

    services = st.session_state.services
    runtime_context = st.session_state.runtime_context

    # --------------------------------------------------
    # Session State
    # --------------------------------------------------

    if "emails" not in st.session_state:
        st.session_state.emails = []

    if "pending_approvals" not in st.session_state:
        st.session_state.pending_approvals = []

    # --------------------------------------------------
    # Refresh Inbox
    # --------------------------------------------------

    if st.button(
        "🔄 Refresh Inbox",
        use_container_width=True,
    ):

        with st.spinner("Fetching unread emails..."):

            st.session_state.emails = (
                services.gmail.fetch_unread_emails()
            )

        st.success(
            f"Fetched {len(st.session_state.emails)} unread emails."
        )

    # --------------------------------------------------
    # Display Emails
    # --------------------------------------------------

    if not st.session_state.emails:

        st.info("No unread emails found.")

        return

    for email in st.session_state.emails:

        with st.expander(email["subject"]):

            st.write(f"**From:** {email['sender']}")
            st.write(f"**Subject:** {email['subject']}")
            st.write(email["body"])

            if st.button(
                "▶ Process",
                key=f"process_{email['id']}",
            ):

                with st.spinner("Running workflow..."):

                    thread_id = (
                        f"THREAD-{uuid4().hex}"
                    )

                    raw_request = (
                        services.gmail
                        .convert_to_raw_request(email)
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

                # -----------------------------------------
                # Error
                # -----------------------------------------

                if result.get("error"):

                    st.error(result["error"])

                    continue

                # -----------------------------------------
                # Human Approval
                # -----------------------------------------

                if "__interrupt__" in result:

                    st.warning(
                        "Waiting for human approval."
                    )

                    st.session_state.pending_approvals.append(
                        {
                            "thread_id": thread_id,
                            "email": email,
                            "result": result,
                        }
                    )

                    continue

                # -----------------------------------------
                # Completed
                # -----------------------------------------

                st.success(
                    result["execution_result"]
                )

                services.gmail.mark_as_processed(
                    email["id"]
                )

                st.session_state.emails.remove(email)

                st.rerun()