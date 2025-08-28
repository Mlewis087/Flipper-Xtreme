"""Whoop device API connector."""
from __future__ import annotations

from typing import Any, Dict

import requests

API_URL = "https://api-7.whoop.com"  # Example base URL


def fetch_metrics(token: str) -> Dict[str, Any]:
    """Fetch metrics from Whoop API.

    Parameters
    ----------
    token: str
        OAuth access token for the user.
    """
    headers = {"Authorization": f"Bearer {token}"}
    try:
        resp = requests.get(f"{API_URL}/cycle", headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException:
        # In production we would log the error details
        return {}
