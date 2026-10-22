"""FastAPI application exposing the joke agent over HTTP."""

import contextlib
from collections.abc import AsyncIterator
from typing import Any

from fastapi import FastAPI, HTTPException
from opentelemetry import trace
from pydantic import BaseModel, Field

from maf.agent import create_joke_agent
from maf.settings import AppSettings, get_settings
from maf.state import SessionStore, conversation_context
from maf.telemetry import configure, create_metrics_app, instrument_asgi

tracer = trace.get_tracer("maf-template")


class ChatRequest(BaseModel):
    """Request to invoke the joke agent."""

    session_id: str = Field(min_length=1)
    message: str = Field(min_length=1)


class ChatResponse(BaseModel):
    """Response from the joke agent."""

    session_id: str
    reply: str


def create_app(settings: AppSettings | None = None) -> Any:
    """Create the FastAPI application for the joke agent."""
    settings = settings or get_settings()
    configure(settings)

    agent = create_joke_agent(settings)
    store = SessionStore()

    @contextlib.asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        yield

    app = FastAPI(title="Maf Template", lifespan=lifespan)
    app.mount("/metrics", create_metrics_app())

    @app.get("/healthz")
    async def healthz() -> dict[str, Any]:
        return {
            "status": "ok",
            "version": settings.app_version,
            "model_enabled": settings.model_is_enabled,
        }

    @app.post("/api/chat", response_model=ChatResponse)
    async def chat(request: ChatRequest) -> ChatResponse:
        state = store.get(request.session_id)
        context = conversation_context(state.history)
        prompt = (
            request.message
            if context == "No prior conversation."
            else f"{context}\n\nCurrent customer message:\n{request.message}"
        )
        with tracer.start_as_current_span("joke_agent.run") as span:
            span.set_attribute("gen_ai.operation.name", "invoke_agent")
            span.set_attribute("gen_ai.agent.name", "Joker")
            span.set_attribute("conversation.id", request.session_id)
            span.set_attribute("chat.message.length", len(request.message))
            try:
                response = await agent.run(prompt)
            except Exception as error:
                raise HTTPException(status_code=502, detail=str(error)) from error
            reply = response.text
        state.history.append((request.message, reply))
        return ChatResponse(session_id=request.session_id, reply=reply)

    return instrument_asgi(app)
