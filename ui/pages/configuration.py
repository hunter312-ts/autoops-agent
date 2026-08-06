from pathlib import Path

import streamlit as st

from app.config.runtime import RuntimeConfig
from app.graph.context import RuntimeContext
from app.services.container import ServiceContainer


def show_configuration_page():
    """
    Configuration page.

    Allows the user to configure the runtime
    services used by AutoOps.
    """

    st.header("⚙️ Configuration")

    st.write(
        "Configure your API keys and Gmail credentials."
    )

    st.divider()

    # --------------------------------------------------
    # Groq API Key
    # --------------------------------------------------

    groq_api_key = st.text_input(
        "Groq API Key",
        type="password",
        help="Enter your Groq API Key.",
    )

    # --------------------------------------------------
    # Gmail Credentials
    # --------------------------------------------------

    uploaded_credentials = st.file_uploader(
        "Upload Gmail credentials.json",
        type=["json"],
    )

    # --------------------------------------------------
    # Save Configuration
    # --------------------------------------------------

    if st.button(
        "💾 Save Configuration",
        use_container_width=True,
    ):

        if not groq_api_key:

            st.error("Please enter your Groq API Key.")

            return

        if uploaded_credentials is None:

            st.error("Please upload credentials.json")

            return

        credentials_path = Path("credentials.json")

        with open(credentials_path, "wb") as f:

            f.write(uploaded_credentials.getbuffer())

        token_path = Path("token.json")

        runtime_config = RuntimeConfig(
            groq_api_key=groq_api_key,
            gmail_credentials_path=credentials_path,
            gmail_token_path=token_path,
        )

        services = ServiceContainer(runtime_config)

        runtime_context = RuntimeContext(
            services=services,
        )

        st.session_state.runtime_config = runtime_config
        st.session_state.runtime_context = runtime_context
        st.session_state.services = services

        st.success("Configuration saved successfully.")

    st.divider()

    # --------------------------------------------------
    # Gmail Authentication
    # --------------------------------------------------

    if st.button(
        "🔐 Authenticate Gmail",
        use_container_width=True,
    ):

        if st.session_state.runtime_config is None:

            st.warning(
                "Save the configuration first."
            )

            return

        try:

            st.session_state.services.gmail.authenticate()

            st.session_state.authenticated = True

            st.success(
                "Gmail authentication successful."
            )

        except Exception as e:

            st.exception(e)

    st.divider()

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    st.subheader("Current Status")

    if st.session_state.runtime_config is None:

        st.error("Configuration not loaded.")

    else:

        st.success("Configuration loaded.")

    if st.session_state.get("authenticated", False):

        st.success("Gmail Connected ✅")

    else:

        st.warning("Gmail Not Connected")