"""
container.py

Central dependency container for AutoOps.

A single ServiceContainer is created for each user session.
It initializes and provides access to all runtime services.
"""

from app.config.runtime import RuntimeConfig
from app.services.gmail_service import GmailService
from app.services.groq_service import GroqService
from app.services.sqlite_service import SQLiteService


class ServiceContainer:
    """
    Holds all runtime services for a single user session.

    Services are initialized once and shared across
    the LangGraph workflow.
    """

    def __init__(self, config: RuntimeConfig):

        self.config = config

        # ---------- AI ----------

        self.groq = GroqService(config)

        # ---------- Gmail ----------

        self.gmail = GmailService(config)

        # ---------- Database ----------

        self.sqlite = SQLiteService()