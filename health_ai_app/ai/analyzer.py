"""Simple AI-powered analyzer for health metrics."""
from __future__ import annotations

from typing import Dict, Any


class AIAnalyzer:
    """Generate feedback from wearable metrics.

    This is a placeholder implementation that uses naive heuristics.
    In production, one could plug in an ML model or external LLM.
    """

    def analyze(self, metrics: Dict[str, Any]) -> str:
        sleep = metrics.get("sleep", {}).get("score")
        strain = metrics.get("strain", {}).get("score")

        suggestions = []
        if sleep is not None and sleep < 70:
            suggestions.append(
                "Your sleep score is below average. Consider winding down earlier tonight."
            )
        if strain is not None and strain > 80:
            suggestions.append(
                "High strain detected. Plan some recovery activities today."
            )
        if not suggestions:
            suggestions.append("Great job! Keep maintaining your habits.")
        return " \n".join(suggestions)
