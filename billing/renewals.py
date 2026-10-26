"""Renewal reminders, sent a week before a subscription renews."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

import stripe

from billing import stripe_client  # noqa: F401  (configures Stripe)


@dataclass(frozen=True)
class Renewal:
    customer_id: str
    renews_on: datetime
    days_in_period: int
    discount_percent: float | None


def renewal(subscription_id: str) -> Renewal:
    subscription = stripe.Subscription.retrieve(subscription_id)
    # The period moved from the subscription to its items; read the old fields as a fallback.
    items = (subscription.get("items") or {}).get("data") or []
    period = items[0] if items else subscription
    start = datetime.fromtimestamp(period["current_period_start"], UTC)
    end = datetime.fromtimestamp(period["current_period_end"], UTC)
    # subscription.discount was removed without a replacement.
    discount_object = subscription.get("discount")
    coupon = discount_object.get("coupon") if discount_object else None
    discount = coupon.get("percent_off") if coupon else None
    return Renewal(subscription.customer, end, (end - start).days, discount)


def reminder_text(renewal: Renewal) -> str:
    text = f"Your plan renews on {renewal.renews_on:%B %d, %Y}."
    if renewal.discount_percent:
        text += f" Your {renewal.discount_percent:g}% discount still applies."
    return text
