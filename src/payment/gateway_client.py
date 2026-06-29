"""
Client for communicating with the external payment gateway.

NOTE: An earlier incident (see
docs/postmortems/postmortem_2024-11-02_gateway_timeout.md) was caused by
relying on the HTTP client library's default timeout, which changed
silently in a minor version bump. As a result, this client now always
sets an explicit timeout on outbound requests.
"""

import requests

GATEWAY_BASE_URL = "https://payments.example-gateway.com/v1"

# Explicit timeout (seconds) — see postmortem 2024-11-02 for why this
# must never be left to the library default.
DEFAULT_TIMEOUT = 30


def charge(payment_data: dict) -> dict:
    """Sends a validated payment payload to the external gateway.

    Args:
        payment_data: validated payment payload (see validator.validate_payment).

    Returns:
        dict: gateway response payload.

    Raises:
        requests.RequestException: on network or gateway errors.
    """
    response = requests.post(
        f"{GATEWAY_BASE_URL}/charge",
        json=payment_data,
        timeout=DEFAULT_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def refund(transaction_id: str) -> dict:
    """Issues a refund for a previously completed transaction."""
    response = requests.post(
        f"{GATEWAY_BASE_URL}/refund",
        json={"transaction_id": transaction_id},
        timeout=DEFAULT_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()
