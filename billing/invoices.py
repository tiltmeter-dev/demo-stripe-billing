"""Invoice summaries for the account page."""

from __future__ import annotations

from typing import Any

import stripe

from billing import stripe_client  # noqa: F401  (configures Stripe)


def invoice_summary(invoice_id: str) -> dict[str, Any]:
    invoice = stripe.Invoice.retrieve(invoice_id, expand=["charge"])
    lines = [
        {"price": line.price.id, "amount": line.amount, "proration": line.proration}
        for line in invoice.lines.data
    ]
    card = invoice.charge.payment_method_details.card.last4 if invoice.charge else None
    return {
        "number": invoice.number,
        "total": invoice.total,
        "lines": lines,
        "prorated": any(line["proration"] for line in lines),
        "card_last4": card,
    }
