from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import pytest
import stripe

from billing import invoices, renewals

SUBSCRIPTION: dict[str, Any] = {
    "id": "sub_1",
    "object": "subscription",
    "customer": "cus_1",
    "current_period_start": 1730419200,  # 2024-11-01
    "current_period_end": 1733011200,  # 2024-12-01
    "discount": {"object": "discount", "coupon": {"object": "coupon", "percent_off": 20.0}},
}

INVOICE: dict[str, Any] = {
    "id": "in_1",
    "object": "invoice",
    "number": "NW-0042",
    "total": 2500,
    "lines": {
        "object": "list",
        "data": [
            {
                "id": "il_1",
                "object": "line_item",
                "amount": 2000,
                "price": {"id": "price_pro", "object": "price"},
                "proration": False,
            },
            {
                "id": "il_2",
                "object": "line_item",
                "amount": 500,
                "price": {"id": "price_seat", "object": "price"},
                "proration": True,
            },
        ],
    },
    "charge": {"id": "ch_1", "object": "charge", "payment_method_details": {"card": {"last4": "4242"}}},
}


@pytest.fixture(autouse=True)
def fake_stripe(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        stripe.Subscription,
        "retrieve",
        lambda *args, **kwargs: stripe.Subscription.construct_from(SUBSCRIPTION, "sk_test"),
    )
    monkeypatch.setattr(
        stripe.Invoice,
        "retrieve",
        lambda *args, **kwargs: stripe.Invoice.construct_from(INVOICE, "sk_test"),
    )


def test_renewal_reminder() -> None:
    renewal = renewals.renewal("sub_1")
    assert renewal.renews_on == datetime(2024, 12, 1, tzinfo=UTC)
    assert renewal.days_in_period == 30
    assert renewals.reminder_text(renewal) == (
        "Your plan renews on December 01, 2024. Your 20% discount still applies."
    )


def test_invoice_summary() -> None:
    summary = invoices.invoice_summary("in_1")
    assert summary["lines"] == [
        {"price": "price_pro", "amount": 2000, "proration": False},
        {"price": "price_seat", "amount": 500, "proration": True},
    ]
    assert summary["prorated"] is True
    assert summary["card_last4"] == "4242"
