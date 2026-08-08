"""
checkpointer.py

Provides the LangGraph checkpoint backend.

The checkpointer stores workflow state whenever the graph
is interrupted, allowing execution to resume later.
"""
import sqlite3
from app.core.config import settings

from langgraph.checkpoint.sqlite import SqliteSaver
from app.core.logging import logger

class GraphCheckpointer:
    """
    Wrapper around LangGraph's SqliteSaver.

    This class centralizes checkpoint configuration so that
    we can easily switch to SQLite/Postgres later.
    """
    def __init__(self):

        logger.info("Initializing LangGraph Checkpointer...")
        db_path = settings.DATABASE_URL.replace(
            "sqlite:///",
            ""
        )

        self.connection = sqlite3.connect(
            db_path,
            check_same_thread=False,
        )

        self.checkpointer = SqliteSaver(self.connection)

    def get_checkpointer(self):

        return self.checkpointer
graph_checkpointer = GraphCheckpointer()