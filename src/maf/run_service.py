"""Run the agent service with uvicorn."""

import os
import sys

import uvicorn

from maf.app import create_app


def main(argv: list[str] | None = None) -> int:
    """Run the FastAPI agent service with uvicorn."""
    args = argv if argv is not None else sys.argv[1:]
    if args:
        raise SystemExit(f"Unexpected arguments for the template service: {args}")
    uvicorn.run(
        create_app,
        factory=True,
        host=os.environ.get("HOST", "0.0.0.0"),
        port=int(os.environ.get("PORT", "8000")),
        log_level=os.environ.get("UVICORN_LOG_LEVEL", "info"),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
