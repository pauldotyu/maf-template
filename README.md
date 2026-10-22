# Microsoft Agent Framework template

A quick start guide for building AI agents using Microsoft's Agent Framework with local LLMs (e.g., Ollama or vLLM).

## Prerequisites

- [Python 3.12+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/) for Python package management
- [Ollama](https://ollama.ai/) installed and running locally
- [vLLM](https://docs.vllm.ai/) (optional, if you want to use vLLM)
- [Docker](https://www.docker.com/) (optional, for observability and Redis)
- [GitHub CLI](https://cli.github.com/) (optional, for cloning the repo)

## Quick Start

This quick start guide will help you set up a simple agent that tells jokes using a local Ollama model. If you prefer to use vLLM, you can skip the Ollama setup and configure the environment variables accordingly.

### 1. Set up Ollama

Pull a model (this example uses gpt-oss:20b, but you can use any model)

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

### 3. Run your first agent

```sh
uv run main.py
```

That's it! Your agent will tell you a joke using your local model.

## Next Steps

- Learn how to enable observability for your agent by following the [Observability Guide](OBSERVABILITY.md)
- Check out the [Agent Framework documentation](https://learn.microsoft.com/agent-framework/tutorials/quick-start?pivots=programming-language-python)
- Explore the [OpenAI chat client source](https://github.com/microsoft/agent-framework/blob/main/python/packages/core/agent_framework/openai/_chat_client.py)
