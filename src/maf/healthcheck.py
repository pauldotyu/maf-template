"""HTTP healthcheck for the agent service."""

import os
import urllib.error
import urllib.request


def main() -> int:
    """Check the /healthz endpoint of the running service."""
    port = int(os.environ.get("PORT", "8000"))
    url = f"http://127.0.0.1:{port}/healthz"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            return 0 if response.status == 200 else 1
    except urllib.error.URLError:
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
