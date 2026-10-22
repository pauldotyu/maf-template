"""HTTP API tests for the FastAPI agent app."""

from types import SimpleNamespace
from typing import Any

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from maf.app import create_app
from maf.settings import AppSettings


class FakeAgent:
    """Minimal stand-in for the real Agent that returns canned jokes."""

    def __init__(self) -> None:
        self.prompts: list[str] = []

    async def run(self, prompt: str, **_: Any) -> Any:
        self.prompts.append(prompt)
        return SimpleNamespace(
            text="Why did the developer go broke? They used up all their cache!"
        )


@pytest.fixture
def app(monkeypatch: pytest.MonkeyPatch) -> FastAPI:
    monkeypatch.setenv("ENABLE_INSTRUMENTATION", "false")
    monkeypatch.setattr("maf.app.create_joke_agent", lambda settings: FakeAgent())
    return create_app(
        AppSettings(app_version="0.0.0-test", openai_base_url="", openai_chat_model="")
    )


@pytest.mark.asyncio
async def test_healthz_returns_ok(app: FastAPI) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "version": "0.0.0-test",
        "model_enabled": False,
    }


@pytest.mark.asyncio
async def test_chat_returns_joke(app: FastAPI) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/chat",
            json={
                "session_id": "session-1",
                "message": "Tell me a dad joke about programming.",
            },
        )

    assert response.status_code == 200
    body = response.json()
    assert body["session_id"] == "session-1"
    assert body["reply"]


@pytest.mark.asyncio
async def test_chat_requires_message(app: FastAPI) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/chat", json={"session_id": "session-1", "message": ""}
        )

    assert response.status_code == 422
