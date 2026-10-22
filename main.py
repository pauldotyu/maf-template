import asyncio
import os

from agent_framework import Agent
from agent_framework.observability import configure_otel_providers
from agent_framework.openai import OpenAIChatClient
from dotenv import load_dotenv

load_dotenv()
enable_instrumentation = os.getenv("ENABLE_INSTRUMENTATION", "false").lower() == "true"
configure_otel_providers(enable_sensitive_data=True) if enable_instrumentation else None


async def main():
    async with (
        Agent(
            client=OpenAIChatClient(),
            name="Joker",
            instructions="You are good at telling jokes.",
        ) as agent,
    ):
        result = await agent.run("Tell me a dad joke about programming.")
        print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
