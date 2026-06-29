"""
Entrypoint for checkout-service.

Exposes the checkout API: validating payment, finalizing the cart, and
charging via the payment gateway.
"""

from flask import Flask, jsonify, request

from src.cart.cart_service import finalize_cart, get_cart
from src.payment.gateway_client import charge
from src.payment.validator import validate_payment

app = Flask(__name__)


@app.route("/checkout/validate", methods=["POST"])
def checkout_validate():
    """Validates a payment payload without charging anything."""
    payment_data = request.get_json(force=True)
    try:
        validate_payment(payment_data)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify({"status": "valid"}), 200


@app.route("/checkout", methods=["POST"])
def checkout():
    """Full checkout flow: validate payment, finalize cart, charge gateway."""
    body = request.get_json(force=True)
    cart_id = body.get("cart_id")
    payment_data = body.get("payment", {})

    try:
        validate_payment(payment_data)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    try:
        get_cart(cart_id)
        finalize_cart(cart_id)
    except KeyError as exc:
        return jsonify({"error": str(exc)}), 404

    try:
        result = charge(payment_data)
    except Exception as exc:  # noqa: BLE001 - surfaced as a 500 intentionally
        return jsonify({"error": f"Gateway error: {exc}"}), 500

    return jsonify({"status": "success", "gateway_response": result}), 200


@app.route("/checkout/confirm", methods=["POST"])
def checkout_confirm():
    """Confirms a previously validated and charged checkout."""
    body = request.get_json(force=True)
    cart_id = body.get("cart_id")
    cart = finalize_cart(cart_id)
    return jsonify({"status": "confirmed", "cart": cart}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
