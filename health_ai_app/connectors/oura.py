"""Oura ring API connector."""
from __future__ import annotations

from typing import Any, Dict

import requests

API_URL = "https://api.ouraring.com/v2"  # Example base URL


def fetch_metrics(token: str) -> Dict[str, Any]:
    """Fetch daily metrics from Oura API."""
    headers = {"Authorization": f"Bearer {token}"}
    try:
        resp = requests.get(f"{API_URL}/usercollection/daily_metrics", headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException:
        return {}
