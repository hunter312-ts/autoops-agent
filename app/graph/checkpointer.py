"""
checkpointer.py

Provides the LangGraph checkpoint backend.

The checkpointer stores workflow state whenever the graph
is interrupted, allowing execution to resume later.
"""
from langgraph.checkpoint.memory import MemorySaver
from app.core.logging import logger

class GraphCheckpointer:
    """
    Wrapper around LangGraph's MemorySaver.

    This class centralizes checkpoint configuration so that
    we can easily switch to SQLite/Postgres later.
    """
    def __init__(self):

        logger.info("Initializing LangGraph Checkpointer...")

        self.memory = MemorySaver()

    def get_checkpointer(self):

        return self.memory
graph_checkpointer = GraphCheckpointer()