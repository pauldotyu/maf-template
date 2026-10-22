# Observability Guide

This guide will help you set up observability for your agent using OpenTelemetry and Grafana's LGTM stack.

## Environment Configuration

The project includes a `.env.example` file that configures the connection to your local LLM.

```properties
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_CHAT_MODEL=gpt-oss:20b
OPENAI_API_KEY=none
ENABLE_INSTRUMENTATION=true
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

- **OPENAI_BASE_URL**: Points to OpenAI API compatible inference server
- **OPENAI_CHAT_MODEL**: The model you want to use
- **OPENAI_API_KEY**: Set to "none" for local servers that don't require authentication
- **ENABLE_INSTRUMENTATION**: Set to `true` to enable OpenTelemetry observability (requires the observability stack below)
- **OTEL_EXPORTER_OTLP_ENDPOINT**: The endpoint for the OpenTelemetry collector

## Optional: Observability with OpenTelemetry and Grafana's LGTM stack

Want to see what's happening under the hood? You can enable observability to monitor your agent's performance.

The docker compose setup also includes Redis for chat history storage if needed.

### Start the monitoring

Start the observability stack

```sh
docker compose -f observability/compose.yaml up -d
```

This will start:

- OpenTelemetry Collector for collecting telemetry data
- Loki for logs
- Grafana for visualization
- Tempo for traces
- Prometheus for metrics
- Redis for chat history storage (not implemented in main.py)

Make sure your `.env` file has observability enabled (this is the default in `.env.example`):

```properties
ENABLE_INSTRUMENTATION=true
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

Run your agent with observability enabled

```sh
uv run main.py
```

View real-time telemetry data with Grafana at [http://localhost:3000](http://localhost:3000).

Click on **Explore** in the sidebar.

Select **Tempo** then click on the **Search** button to see traces.

You should see traces, metrics, and logs related to your agent's operations.

The telemetry shows you:

- **Traces**: How your agent processes requests
- **Metrics**: Token usage and performance data
- **Logs**: Debug information and agent activities

### Stop monitoring

To stop the observability stack and remove volumes, run:

```sh
docker compose -f observability/compose.yaml down -v
```

## Check stored chat messages

If you're using Redis for chat history storage, you can view the stored messages using the Redis CLI or the VS Code extension for Redis.
