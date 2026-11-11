"""Minimal client for the Redfin API on RapidAPI.

Set RAPIDAPI_KEY in your environment (or in a .env file at the repo root).
"""

import os
from datetime import datetime, timedelta, timezone

import requests

HOST = "redfin16.p.rapidapi.com"


def _load_dotenv():
    """Read RAPIDAPI_KEY from a .env in the current folder or the repo root, if present."""
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
    for path in (".env", os.path.join(root, ".env")):
        if os.path.exists(path):
            for line in open(path, encoding="utf-8"):
                key, sep, value = line.strip().partition("=")
                if sep and value and not key.startswith("#"):
                    os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()


def get(path, **params):
    """GET an endpoint and return the `data` object of the response."""
    key = os.environ.get("RAPIDAPI_KEY")
    if not key:
        raise SystemExit("Set RAPIDAPI_KEY first (see .env.example).")
    response = requests.get(
        f"https://{HOST}{path}",
        params={k: v for k, v in params.items() if v is not None},
        headers={"x-rapidapi-host": HOST, "x-rapidapi-key": key},
        timeout=60,
    )
    response.raise_for_status()
    body = response.json()
    if not body.get("success", True):
        raise RuntimeError(f"{path} failed: {body}")
    return body["data"]


def to_date(value):
    """Redfin dates come in three shapes: ISO strings on search cards, Unix seconds on
    sold comps, and Unix milliseconds in price history and estimates."""
    if value is None:
        return None
    if isinstance(value, str):
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    seconds = value / 1000 if value > 10**11 else value
    return datetime.fromtimestamp(seconds, tz=timezone.utc).date()


def current_listing_events(history, listed_date):
    """The events of a home's current listing, newest first, without duplicates.

    `listed_date` is the search card's `listedDate`. priceHistory mixes every listing the
    home ever had (old sales, rentals), lists some events twice (once per source, such as
    the MLS and Zillow), and for some homes has not caught up with the current listing at
    all. Keeping only events from the listing date on handles all three: when the history
    lags, the result is simply empty.
    """
    start = to_date(listed_date)
    seen, events = set(), []
    for event in history.get("priceHistory") or []:
        day = to_date(event["date"])
        if start is None or day < start - timedelta(days=3):
            continue
        key = (day, event["event"], event["price"])
        if key not in seen:
            seen.add(key)
            events.append(event)
    return events


def median(values):
    values = sorted(v for v in values if v is not None)
    if not values:
        return None
    mid = len(values) // 2
    return values[mid] if len(values) % 2 else (values[mid - 1] + values[mid]) / 2
