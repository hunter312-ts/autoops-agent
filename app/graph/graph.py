from langgraph.graph import StateGraph, START, END
from app.graph.state import AgentState
from app.graph.router import router, route_decision
from app.graph.checkpointer import graph_checkpointer
from app.nodes.ingest import ingest_request
from app.nodes.classify import classify_node
from app.nodes.execute import execute_node
from app.nodes.approve import approve_node
from app.nodes.log import log_node
from app.graph.context import RuntimeContext

builder = StateGraph(AgentState,context_schema=RuntimeContext,)

# ---------------- Nodes ----------------

builder.add_node("ingest", ingest_request)
builder.add_node("classify", classify_node)
builder.add_node("router", router)
builder.add_node("execute", execute_node)
builder.add_node("approve", approve_node)
builder.add_node("log", log_node)

# ---------------- Linear Flow ----------------

builder.add_edge(START, "ingest")
builder.add_edge("ingest", "classify")
builder.add_edge("classify", "router")

# ---------------- Conditional Flow ----------------

builder.add_conditional_edges(
    "router",
    route_decision,
    {
        "AUTO_REPLY": "execute",
        "CREATE_TICKET": "execute",
        "HUMAN_APPROVAL": "approve",
    },
)

# ---------------- Finish Flow ----------------
builder.add_edge("approve", "execute")
builder.add_edge("execute", "log")
builder.add_edge("log", END)

graph = builder.compile(checkpointer=graph_checkpointer.get_checkpointer())