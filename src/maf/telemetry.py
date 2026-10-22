"""OpenTelemetry and Prometheus wiring for the agent service."""

import logging
from typing import Any

from agent_framework.observability import configure_otel_providers
from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware
from prometheus_client import make_asgi_app

from maf.settings import AppSettings


def configure(settings: AppSettings) -> None:
    """Configure logging and OpenTelemetry exporters from application settings."""
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    if not settings.enable_instrumentation:
        return
    configure_otel_providers(enable_sensitive_data=True)


def create_metrics_app() -> Any:
    """Return the Prometheus ASGI app for the /metrics endpoint."""
    return make_asgi_app()


def instrument_asgi(app: Any) -> Any:
    """Instrument an ASGI app with OpenTelemetry."""
    return OpenTelemetryMiddleware(
        app,
        excluded_urls=r".*/healthz$|.*/metrics/?$",
        exclude_spans=["receive", "send"],
    )
