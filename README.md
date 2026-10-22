# Microsoft Agent Framework template

A minimal template for running an AI agent as a long-lived service with the Microsoft Agent Framework, OpenAI-compatible models, and FastAPI.

The template runs a single "Joker" agent that tells dad jokes. Instead of a one-shot script, the agent lives behind a small FastAPI service so dev tools, browsers, and other services can invoke it over HTTP.

## Prerequisites

- [Python 3.12+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/) for Python package management
- [Ollama](https://ollama.ai/) installed and running locally, or [vLLM](https://docs.vllm.ai/)
- [Docker](https://www.docker.com/) (optional, for observability)

## Quick Start

This quick start sets up a simple agent that tells dad jokes using a local Ollama model.

### 1. Set up Ollama

Pull a model (this example uses `gpt-oss:20b`, but you can use any model)

```sh
ollama pull gpt-oss:20b
```

Verify the model is available

```sh
ollama list
```

### 2. Create your project

Clone this repository or create a new project

```sh
gh repo create demo --template pauldotyu/maf-template --clone --private
cd demo
```

Install dependencies

```sh
uv sync
```

Create a `.env` file by copying the provided example

```sh
cp .env.example .env
```

### 3. Run the service

```sh
uv run maf-serve
```

The service starts on http://localhost:8000 and the agent will tell you a dad joke.

### 3b. Run the service with Docker

Build and run the service container:

```sh
docker build -t maf-template .
docker run -p 8000:8000 --env-file .env maf-template
```

The service starts on http://localhost:8000 and the agent will tell you a dad joke.

## Endpoints

- `GET /healthz` — liveness probe for the service
- `POST /api/chat` — invoke the joke agent; returns the joke the agent came up with
- `GET /metrics` — Prometheus metrics scrape endpoint

Invoke the model:

```sh
curl -s -X POST http://localhost:8000/api/chat \
  -H 'content-type: application/json' \
  -d '{"session_id":"demo-1","message":"Tell me a dad joke about programming."}'
```

Response:

```json
{ "session_id": "demo-1", "reply": "Why did the developer go broke? They used up all their cache!" }
```

## Development

- Run tests: `uv run pytest`
- Lint: `uv run ruff check .`
- Format: `uv run ruff format .`
- Type check: `uv run pyright`

## Observability

- Learn how to enable observability for your agent by following the [Observability Guide](OBSERVABILITY.md)
- Check out the [Agent Framework documentation](https://learn.microsoft.com/agent-framework/tutorials/quick-start?pivots=programming-language-python)
- Explore the [OpenAI chat client source](https://github.com/microsoft/agent-framework/blob/main/python/packages/core/agent_framework/openai/_chat_client.py)