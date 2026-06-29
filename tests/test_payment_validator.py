"""
Unit tests for payment validation logic.

NOTE: test_validate_payment_legacy_short_token is expected to FAIL on the
current main branch due to the card_token length regression described in
docs/postmortems/postmortem_2025-03-14_payment_validation_500s.md. it is
included here intentionally to demonstrate the gap in the original test
suite (the staging tests used tokens >10 chars and never caught this).
"""

import pytest

from src.payment.validator import validate_payment


def test_validate_payment_valid_token():
    payment_data = {"card_token": "tok_1234567890abcdef", "amount": 49.99}
    assert validate_payment(payment_data) is True


def test_validate_payment_missing_token():
    payment_data = {"amount": 49.99}
    with pytest.raises(ValueError, match="card_token"):
        validate_payment(payment_data)


def test_validate_payment_invalid_amount():
    payment_data = {"card_token": "tok_1234567890abcdef", "amount": 0}
    with pytest.raises(ValueError, match="Invalid amount"):
        validate_payment(payment_data)


def test_validate_payment_legacy_short_token():
    """Legacy/staging-style short tokens (<10 chars) used to be valid.

    This currently FAILS on main due to the stricter length check added
    in the "Refactor payment validation logic" commit. See Issue #2 and
    the open PR "Relax card_token length check..." for the proposed fix.
    """
    payment_data = {"card_token": "tok_123", "amount": 49.99}
    assert validate_payment(payment_data) is True
