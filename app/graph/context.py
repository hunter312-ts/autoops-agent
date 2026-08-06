"""
context.py

Defines the runtime context passed to every LangGraph node.

Unlike AgentState, the runtime context is NOT checkpointed.
It contains long-lived services and dependencies that are
shared across the workflow.
"""

from dataclasses import dataclass

from app.services.container import ServiceContainer


@dataclass
class RuntimeContext:
    """
    Runtime dependencies available to all LangGraph nodes.

    These objects are injected at graph execution time and
    are not stored in the graph state.
    """

    services: ServiceContainer