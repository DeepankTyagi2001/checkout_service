# checkout-service

Handles cart finalization and payment processing for the platform's checkout flow.

## Overview

`checkout-service` validates incoming payment requests, coordinates with the
cart service to finalize order contents, and forwards validated payment
payloads to the external payment gateway.

## Structure

- `src/payment/` — payment validation and gateway client logic
- `src/cart/` — cart retrieval and finalization logic
- `src/main.py` — service entrypoint / API routes
- `tests/` — unit tests

## Running locally

```bash
pip install -r requirements.txt
python src/main.py
```

## Key endpoints

- `POST /checkout` — initiate checkout for a given cart
- `POST /checkout/validate` — validate payment payload only
- `POST /checkout/confirm` — confirm and finalize a checkout after validation

## Related docs

See `docs/postmortems/` for past incident history, and `docs/runbook_checkout_5xx_errors.md`
for on-call troubleshooting steps.
