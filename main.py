import asyncio

from agent_framework import Agent
from agent_framework.observability import configure_otel_providers
from agent_framework.openai import OpenAIChatClient
from dotenv import load_dotenv

load_dotenv()
configure_otel_providers(enable_sensitive_data=True)


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
