# AI Agent Development Instructions

## Project Overview

This project uses Python with `uv` for package management, the Microsoft Agent Framework, OpenAI-compatible models, FastAPI, and uvicorn.

## Development Environment

### Package Management

- Use `uv` for all Python package management operations
- Run `uv sync` to install dependencies from `pyproject.toml`
- Run `uv add <package>` to add new dependencies
- Run `uv remove <package>` to remove dependencies
- Use `uv run <command>` to execute commands in the virtual environment
- Never use `pip` directly; always use `uv` equivalents

### Commands

- `uv sync` — install dependencies
- `uv run maf-serve` — run the agent service via uvicorn
- `uv run maf-healthcheck` — run the HTTP healthcheck against the service
- `uv run pytest` — run tests
- `uv run ruff check .` — lint
- `uv run ruff format .` — format
- `uv run pyright` — type check

### Python Version

- Specify Python version in `pyproject.toml` under `[project]` section
- Use `uv python install <version>` to install specific Python versions
- Use `uv python pin <version>` to pin the project to a specific Python version

## Architecture

- Package code lives in `src/maf/` (src layout) and is installed as the `maf` package.
- `src/maf/settings.py` — `AppSettings` loaded from environment variables.
- `src/maf/model_client.py` — OpenAI-compatible chat completion client factory (`OpenAIAuthMode`).
- `src/maf/agent.py` — `create_joke_agent(settings)` builds the `Agent`.
- `src/maf/state.py` — in-process session store and conversation context helpers.
- `src/maf/app.py` — FastAPI app factory `create_app(settings)` exposing `GET /healthz`, `POST /api/chat`, and `GET /metrics`.
- `src/maf/run_service.py` — uvicorn entry point behind the `maf-serve` console script.
- `src/maf/healthcheck.py` — HTTP healthcheck behind the `maf-healthcheck` console script.
- `src/maf/telemetry.py` — OpenTelemetry setup and Prometheus metrics app helpers.

## Environment Variables

- `OPENAI_BASE_URL` — OpenAI-compatible endpoint (default `http://localhost:11434/v1`)
- `OPENAI_CHAT_MODEL` — model name (default `qwen3:8b`)
- `OPENAI_AUTH_MODE` — `api_key`, `default_credential`, or `workload_identity`
- `OPENAI_API_KEY` — API key for `api_key` auth mode
- `ENABLE_INSTRUMENTATION` — toggle OpenTelemetry setup
- `OTEL_EXPORTER_OTLP_ENDPOINT` — OTLP collector endpoint

## Conventions

- Prefer the agent-framework abstractions (agents, sessions, middleware) over hand-rolled loops.
- Keep HTTP contracts in FastAPI Pydantic models in the app module.
- Keep tests in `tests/` using `httpx.ASGITransport` with fake agents, no live model calls.