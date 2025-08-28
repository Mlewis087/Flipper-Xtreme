"""Minimal subscription management utilities."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict


@dataclass
class Subscription:
    user_id: str
    expires_at: datetime

    def is_active(self) -> bool:
        return datetime.utcnow() < self.expires_at


class SubscriptionService:
    """Keep track of user subscriptions in memory."""

    def __init__(self) -> None:
        self._subs: Dict[str, Subscription] = {}

    def add_subscription(self, user_id: str, days: int = 30) -> None:
        self._subs[user_id] = Subscription(user_id, datetime.utcnow() + timedelta(days=days))

    def is_active(self, user_id: str) -> bool:
        sub = self._subs.get(user_id)
        return sub.is_active() if sub else False
