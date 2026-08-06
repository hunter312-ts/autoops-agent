import streamlit as st
import pandas as pd
import sqlite3

from app import services


DATABASE = "autoops.db"


def show_history_page():
    """
    Workflow History Dashboard.

    Displays all processed workflows stored in SQLite.
    """

    st.header("📊 Workflow History")

    # --------------------------------------------------
    # Refresh
    # --------------------------------------------------

    if st.button(
        "🔄 Refresh History",
        use_container_width=True,
    ):
        st.rerun()

    st.divider()

    try:
        services = st.session_state.services

        conn = services.sqlite.get_connection()

        query = """
            SELECT
                request_id,
                sender,
                source,
                intent,
                confidence,
                risk,
                route,
                approval,
                execution_result AS execution,
                error,
                created_at
            FROM workflow_logs
            ORDER BY created_at DESC;
            """

        df = pd.read_sql_query(query, conn)

        conn.close()

    except Exception as e:

        st.error(e)

        return

    # --------------------------------------------------
    # No Records
    # --------------------------------------------------

    if df.empty:

        st.info("No workflow history found.")

        return

    # --------------------------------------------------
    # Metrics
    # --------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Requests",
            len(df),
        )

    with col2:

        st.metric(
            "Auto Replies",
            len(
                df[df["route"] == "AUTO_REPLY"]
            ),
        )

    with col3:

        st.metric(
            "Tickets",
            len(
                df[df["route"] == "CREATE_TICKET"]
            ),
        )

    with col4:

        st.metric(
            "Human Approval",
            len(
                df[df["route"] == "HUMAN_APPROVAL"]
            ),
        )

    st.divider()

    # --------------------------------------------------
    # Filters
    # --------------------------------------------------

    routes = ["All"] + sorted(
        df["route"].dropna().unique().tolist()
    )

    selected_route = st.selectbox(
        "Filter by Route",
        routes,
    )

    if selected_route != "All":

        df = df[
            df["route"] == selected_route
        ]

    # --------------------------------------------------
    # Table
    # --------------------------------------------------

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )