import streamlit as st

from ui.pages.configuration import show_configuration_page
from ui.pages.inbox import show_inbox_page
from ui.pages.approvals import show_approvals_page
from ui.pages.history import show_history_page


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AutoOps AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# Session State Initialization
# --------------------------------------------------

if "runtime_config" not in st.session_state:
    st.session_state.runtime_config = None

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.title("🤖 AutoOps AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "⚙️ Configuration",
        "📬 Inbox",
        "👨 Human Approval",
        "📊 History",
    ],
)

st.sidebar.markdown("---")

st.sidebar.success(
    "Backend Status: Online"
)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🤖 AutoOps AI Dashboard")
st.caption(
    "AI-powered customer support automation using LangGraph."
)

# --------------------------------------------------
# Navigation
# --------------------------------------------------

if page == "⚙️ Configuration":
    show_configuration_page()

elif page == "📬 Inbox":
    show_inbox_page()

elif page == "👨 Human Approval":
    show_approvals_page()

elif page == "📊 History":
    show_history_page()