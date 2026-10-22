from agent_framework import Agent
from agent_framework.devui import serve
from agent_framework.observability import configure_otel_providers
from agent_framework.openai import OpenAIChatClient
from dotenv import load_dotenv

load_dotenv()
configure_otel_providers(enable_sensitive_data=True)


def get_weather(location: str) -> str:
    """Get weather for a location."""
    return f"Weather in {location}: 72F and sunny"


# Create your agent
agent = Agent(name="WeatherAgent", client=OpenAIChatClient(), tools=[get_weather])


serve(entities=[agent], auto_open=True)
