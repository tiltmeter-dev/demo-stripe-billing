# Northwind Billing

Renewal reminders and invoice summaries for Northwind's subscriptions, from Stripe.

Written in mid-2024 against Stripe API version `2024-06-20`, through stripe-python 10.

```bash
uv run --no-project --with-requirements requirements.txt --with pytest python -m pytest -q
```

## A Tiltmeter demo

This code still reads Stripe's 2024 response shapes. [Tiltmeter](https://github.com/tiltmeter-dev/tiltmeter)
follows Stripe's real OpenAPI spec (`tiltmeter.yaml`), compares the version this code was
written for with today's, and the `API changes` workflow opens a pull request that adapts
the code. The agent's edits are tested before the pull request opens.
