from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class EconomicEvent:
    title: str
    currency: str
    impact: str
    event_time: datetime

    @property
    def display_title(self) -> str:
        return f"{self.title} - {self.currency}"