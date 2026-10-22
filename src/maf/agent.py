"""Joke agent built on the OpenAI-compatible chat completion client."""

from agent_framework import Agent

from maf.model_client import create_openai_chat_client
from maf.settings import AppSettings

JOKE_INSTRUCTIONS = "You are good at telling jokes."


def create_joke_agent(settings: AppSettings) -> Agent:
    """Create the joke agent for the configured model endpoint."""
    client = create_openai_chat_client(
        model=settings.openai_chat_model,
        base_url=settings.openai_base_url,
        auth_mode=settings.openai_auth_mode,
        api_key=settings.openai_api_key,
    )
    return Agent(
        client=client,
        name="Joker",
        instructions=JOKE_INSTRUCTIONS,
        default_options={"temperature": 0.7, "max_tokens": 200},
    )
