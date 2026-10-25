"""Stripe settings shared by every billing module."""

from __future__ import annotations

import os

import stripe

stripe.api_key = os.environ.get("STRIPE_API_KEY", "")
# stripe-python 10 pins this version; it is set here too so that upgrades are deliberate.
stripe.api_version = "2024-06-20"
