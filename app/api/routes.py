from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter

from app.api.models import ProcessRequest
from app.config.runtime import RuntimeConfig
from app.graph.context import RuntimeContext
from app.graph.graph import graph
from app.services.container import ServiceContainer

router = APIRouter()


@router.post("/process")
def process_request(request: ProcessRequest):

    runtime_config = RuntimeConfig(
        groq_api_key=request.groq_api_key,
        gmail_credentials_path=Path(request.gmail_credentials_path),
        gmail_token_path=Path(request.gmail_token_path),
    )

    services = ServiceContainer(runtime_config)

    runtime_context = RuntimeContext(
        services=services,
    )

    thread_id = f"THREAD-{uuid4().hex}"

    state = {
        "thread_id": thread_id,
        "raw_request": {
            "source": request.source,
            "sender": request.sender,
            "subject": request.subject,
            "body": request.body,
        },
        "request": None,
        "classification": None,
        "route": None,
        "approval": None,
        "execution_result": None,
        "error": None,
    }

    result = graph.invoke(
        state,
        context=runtime_context,
        config={
            "configurable": {
                "thread_id": thread_id
            }
        },
    )

    return {
        "status": "success",
        "result": result,
    }