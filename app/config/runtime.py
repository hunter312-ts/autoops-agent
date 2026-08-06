"""
runtime.py

Defines the runtime configuration for a user session.

Unlike .env settings, these values are provided by the
frontend (Streamlit) at runtime and are not hardcoded
into the backend.
"""

from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


class RuntimeConfig(BaseModel):
    """
    Runtime configuration for the current user session.
    """

    # --------------------------------------------------
    # AI Configuration
    # --------------------------------------------------

    groq_api_key: str = Field(
        ...,
        description="Groq API key supplied by the user.",
    )

    model: str = Field(
        default="llama-3.3-70b-versatile",
        description="Groq model to use.",
    )

    temperature: float = Field(
        default=0.0,
        ge=0.0,
        le=2.0,
        description="LLM temperature.",
    )

    # --------------------------------------------------
    # Gmail Configuration
    # --------------------------------------------------

    gmail_credentials_path: Optional[Path] = Field(
        default=None,
        description="Path to the Gmail OAuth credentials.json file.",
    )

    gmail_token_path: Optional[Path] = Field(
        default=None,
        description="Path to the Gmail token.json file.",
    )

    # --------------------------------------------------
    # LangSmith Configuration
    # --------------------------------------------------

    langsmith_api_key: Optional[str] = Field(
        default=None,
        description="Optional LangSmith API key.",
    )

    langsmith_project: str = Field(
        default="AutoOps-Agent",
        description="LangSmith project name.",
    )