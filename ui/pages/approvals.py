import streamlit as st
from langgraph.types import Command

from app.graph.graph import graph


def show_approvals_page():
    """
    Human Approval Dashboard.

    Displays all interrupted workflows and allows
    an operator to approve or reject them.
    """

    st.header("👨 Human Approval")

    # --------------------------------------------------
    # Check Configuration
    # --------------------------------------------------

    if st.session_state.runtime_config is None:

        st.warning("Please configure AutoOps first.")

        return

    if "pending_approvals" not in st.session_state:

        st.session_state.pending_approvals = []

    if len(st.session_state.pending_approvals) == 0:

        st.success("No pending approvals.")

        return

    runtime_context = st.session_state.runtime_context
    services = st.session_state.services

    # --------------------------------------------------
    # Pending Requests
    # --------------------------------------------------

    for approval in st.session_state.pending_approvals.copy():

        email = approval["email"]

        interrupt = approval["result"]["__interrupt__"][0]

        data = interrupt.value

        with st.container(border=True):

            st.subheader(data["subject"])

            col1, col2 = st.columns(2)

            with col1:

                st.write(f"**Sender:** {data['sender']}")

                st.write(f"**Intent:** {data['intent']}")

            with col2:

                st.write(f"**Risk:** {data['risk']}")

                st.write(f"**Request ID:** {data['request_id']}")

            st.info(data["reason"])

            approve_col, reject_col = st.columns(2)

            # --------------------------------------------------
            # Approve
            # --------------------------------------------------

            with approve_col:

                if st.button(
                    "✅ Approve",
                    key=f"approve_{data['request_id']}",
                    use_container_width=True,
                ):

                    result = graph.invoke(
                        Command(resume=True),
                        context=runtime_context,
                        config={
                            "configurable": {
                                "thread_id": approval["thread_id"]
                            }
                        },
                    )

                    if result.get("error"):

                        st.error(result["error"])

                    else:

                        services.gmail.mark_as_processed(
                            email["id"]
                        )

                        st.success(
                            "Workflow completed successfully."
                        )

                        st.session_state.pending_approvals.remove(
                            approval
                        )

                        st.rerun()

            # --------------------------------------------------
            # Reject
            # --------------------------------------------------

            with reject_col:

                if st.button(
                    "❌ Reject",
                    key=f"reject_{data['request_id']}",
                    use_container_width=True,
                ):

                    result = graph.invoke(
                        Command(resume=False),
                        context=runtime_context,
                        config={
                            "configurable": {
                                "thread_id": approval["thread_id"]
                            }
                        },
                    )

                    st.warning(
                        "Workflow rejected."
                    )

                    st.session_state.pending_approvals.remove(
                        approval
                    )

                    st.rerun()