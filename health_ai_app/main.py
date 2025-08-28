"""Demo CLI for the health AI app."""
from __future__ import annotations

import os
from typing import Dict, Any

from .connectors import whoop, oura, apple_fitness
from .ai.analyzer import AIAnalyzer
from .subscription import SubscriptionService


def gather_metrics(tokens: Dict[str, str]) -> Dict[str, Any]:
    """Collect metrics from all supported services."""
    metrics: Dict[str, Any] = {}
    if token := tokens.get("whoop"):
        metrics["whoop"] = whoop.fetch_metrics(token)
    if token := tokens.get("oura"):
        metrics["oura"] = oura.fetch_metrics(token)
    if token := tokens.get("apple"):
        metrics["apple"] = apple_fitness.fetch_metrics(token)
    # Normalize some values for analysis
    return {
        "sleep": metrics.get("oura", {}).get("data", [{}])[0].get("sleep_score"),
        "strain": metrics.get("whoop", {}).get("strain_score"),
    }


def main() -> None:
    user_id = os.getenv("USER_ID", "demo-user")
    tokens = {
        "whoop": os.getenv("WHOOP_TOKEN", ""),
        "oura": os.getenv("OURA_TOKEN", ""),
        "apple": os.getenv("APPLE_TOKEN", ""),
    }

    subscriptions = SubscriptionService()
    subscriptions.add_subscription(user_id)
    if not subscriptions.is_active(user_id):
        print("Subscription inactive. Please renew to receive insights.")
        return

    metrics = gather_metrics(tokens)
    analyzer = AIAnalyzer()
    feedback = analyzer.analyze(metrics)
    print("Feedback:\n" + feedback)


if __name__ == "__main__":
    main()
