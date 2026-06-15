from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

from core.event_model import EconomicEvent


FOREX_FACTORY_URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"

BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = BASE_DIR / "data" / "cache"
CACHE_PATH = CACHE_DIR / "forexfactory_thisweek.json"


class ForexFactoryError(Exception):
    pass


@dataclass(frozen=True)
class ForexFactoryResult:
    events: list[EconomicEvent]
    source: str
    total_received: int
    today_count: int
    currency_count: int
    impact_count: int
    time_window_count: int
    cache_message: str = ""


def fetch_forexfactory_events(
    timezone_name: str,
    currencies: list[str],
    impacts: list[str],
    active_start: str,
    active_end: str,
    force_refresh: bool = False,
) -> ForexFactoryResult:
    """
    Fetches ForexFactory economic calendar with local cache fallback.

    Current MVP behavior:
    - Loads today's events.
    - Filters by selected currencies.
    - Filters by selected impact levels.
    - Does NOT filter by active_start / active_end.
    - active_start and active_end remain in the signature for compatibility
      with the current UI/main_window.py.
    """

    local_tz = ZoneInfo(timezone_name)

    if not force_refresh:
        cached_payload = _load_cache_if_valid(local_tz=local_tz)

        if cached_payload is not None:
            return _parse_events(
                raw_events=cached_payload["events"],
                timezone_name=timezone_name,
                currencies=currencies,
                impacts=impacts,
                source="CACHE",
                cache_message="Cache válido del día.",
            )

    try:
        raw_events = _fetch_from_web()
        _save_cache(raw_events=raw_events, local_tz=local_tz)

        return _parse_events(
            raw_events=raw_events,
            timezone_name=timezone_name,
            currencies=currencies,
            impacts=impacts,
            source="WEB",
            cache_message="Descarga nueva desde ForexFactory.",
        )

    except ForexFactoryError as exc:
        cached_payload = _load_any_cache()

        if cached_payload is not None:
            return _parse_events(
                raw_events=cached_payload["events"],
                timezone_name=timezone_name,
                currencies=currencies,
                impacts=impacts,
                source="CACHE_FALLBACK",
                cache_message=f"Web falló. Usando cache local. Detalle: {exc}",
            )

        raise


def _fetch_from_web() -> list[dict]:
    try:
        response = requests.get(
            FOREX_FACTORY_URL,
            timeout=15,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "Chrome/120.0.0.0 "
                    "Safari/537.36"
                ),
                "Accept": "application/json,text/plain,*/*",
                "Accept-Language": "en-US,en;q=0.9,es-MX;q=0.8,es;q=0.7",
                "Cache-Control": "no-cache",
            },
        )
        response.raise_for_status()

    except requests.RequestException as exc:
        raise ForexFactoryError(f"No se pudo consultar ForexFactory: {exc}") from exc

    try:
        raw_events = response.json()
    except ValueError as exc:
        raise ForexFactoryError("ForexFactory no devolvió JSON válido.") from exc

    if not isinstance(raw_events, list):
        raise ForexFactoryError("ForexFactory devolvió una estructura inesperada.")

    return raw_events


def _save_cache(raw_events: list[dict], local_tz: ZoneInfo) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    payload = {
        "cached_at": datetime.now(tz=local_tz).isoformat(),
        "events": raw_events,
    }

    with CACHE_PATH.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)


def _load_cache_if_valid(local_tz: ZoneInfo) -> dict | None:
    payload = _load_any_cache()

    if payload is None:
        return None

    cached_at_raw = payload.get("cached_at")

    if not cached_at_raw:
        return None

    try:
        cached_at = datetime.fromisoformat(cached_at_raw).astimezone(local_tz)
    except ValueError:
        return None

    today_local = datetime.now(tz=local_tz).date()

    if cached_at.date() != today_local:
        return None

    return payload


def _load_any_cache() -> dict | None:
    if not CACHE_PATH.exists():
        return None

    try:
        with CACHE_PATH.open("r", encoding="utf-8") as file:
            payload = json.load(file)

        if not isinstance(payload, dict):
            return None

        if "events" not in payload:
            return None

        if not isinstance(payload["events"], list):
            return None

        return payload

    except (json.JSONDecodeError, OSError):
        return None


def _parse_events(
    raw_events: list[dict],
    timezone_name: str,
    currencies: list[str],
    impacts: list[str],
    source: str,
    cache_message: str = "",
) -> ForexFactoryResult:
    local_tz = ZoneInfo(timezone_name)
    today_local = datetime.now(tz=local_tz).date()

    currencies_set = {currency.upper() for currency in currencies}
    impacts_set = {_normalize_impact(impact) for impact in impacts}

    total_received = len(raw_events)
    today_count = 0
    currency_count = 0
    impact_count = 0
    shown_count = 0

    filtered_events: list[EconomicEvent] = []

    for item in raw_events:
        try:
            title = str(item.get("title", "")).strip()
            currency = str(item.get("country", "")).strip().upper()
            impact = _normalize_impact(str(item.get("impact", "")).strip())
            raw_date = str(item.get("date", "")).strip()

            if not title or not currency or not impact or not raw_date:
                continue

            event_time_source = datetime.fromisoformat(raw_date)
            event_time_local = event_time_source.astimezone(local_tz)

            if event_time_local.date() != today_local:
                continue

            today_count += 1

            if currency not in currencies_set:
                continue

            currency_count += 1

            if impact not in impacts_set:
                continue

            impact_count += 1
            shown_count += 1

            filtered_events.append(
                EconomicEvent(
                    title=title,
                    currency=currency,
                    impact=impact,
                    event_time=event_time_local,
                )
            )

        except Exception:
            continue

    return ForexFactoryResult(
        events=sorted(filtered_events, key=lambda event: event.event_time),
        source=source,
        total_received=total_received,
        today_count=today_count,
        currency_count=currency_count,
        impact_count=impact_count,
        time_window_count=shown_count,
        cache_message=cache_message,
    )


def _normalize_impact(impact: str) -> str:
    impact = impact.strip().lower()

    if impact == "high":
        return "High"

    if impact == "medium":
        return "Medium"

    if impact == "low":
        return "Low"

    if impact == "holiday":
        return "Holiday"

    return impact.capitalize()