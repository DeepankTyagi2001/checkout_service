"""
Payment validation logic for checkout-service.

NOTE: A stricter card_token length check was introduced in the
"Refactor payment validation logic" commit. This is the change suspected
of causing the recent spike in checkout 500 errors (see Issue #1, #2 and
docs/postmortems/postmortem_2025-03-14_payment_validation_500s.md).

A fix is proposed in an open PR ("Relax card_token length check...") but
has not yet been merged into main.
"""


def validate_payment(payment_data: dict) -> bool:
    """Validates payment payload before sending to gateway.

    Args:
        payment_data: dict expected to contain at least 'card_token' and
            'amount'.

    Returns:
        True if validation passes.

    Raises:
        ValueError: if the payload is missing required fields or fails
            validation checks.
    """
    card_token = payment_data.get("card_token")

    # NOTE: this length check was added in a recent refactor and is the
    # suspected root cause of the current incident. Legacy/test tokens
    # shorter than 10 characters are being rejected.


    # if not card_token or len(card_token) < 10:
    #     raise ValueError("Missing or malformed card_token")

    # if payment_data.get("amount", 0) <= 0:
    #     raise ValueError("Invalid amount")

    # return True

    card_token = payment_data.get("card_token")
    if not card_token or len(card_token) < 10:   # <-- new stricter check
        raise ValueError("Missing or malformed card_token")
    if payment_data.get("amount", 0) <= 0:
        raise ValueError("Invalid amount")
    return True
