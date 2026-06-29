"""
Cart retrieval and finalization logic.

NOTE: This module previously used an unbounded module-level dict as a
cache, which caused a memory leak and repeated pod OOMKills (see
docs/postmortems/postmortem_2025-01-20_cart_memory_leak.md). It now uses
a bounded TTL cache instead.
"""

from cachetools import TTLCache

# Bounded cache with a 5-minute TTL and max 10k entries — replaces the
# old unbounded dict that caused the 2025-01-20 incident.
_cart_cache = TTLCache(maxsize=10_000, ttl=300)


def get_cart(cart_id: str) -> dict:
    """Fetches a cart by ID, using a short-lived cache.

    Args:
        cart_id: unique identifier for the cart.

    Returns:
        dict representing the cart contents.

    Raises:
        KeyError: if the cart does not exist.
    """
    if cart_id in _cart_cache:
        return _cart_cache[cart_id]

    # In a real implementation this would query a cart database/service
    cart = _fetch_cart_from_store(cart_id)
    _cart_cache[cart_id] = cart
    return cart


def finalize_cart(cart_id: str) -> dict:
    """Marks a cart as finalized ahead of payment processing."""
    cart = get_cart(cart_id)
    cart["status"] = "finalized"
    _cart_cache[cart_id] = cart
    return cart


def _fetch_cart_from_store(cart_id: str) -> dict:
    """Placeholder for the real cart data store lookup."""
    if not cart_id:
        raise KeyError("cart_id is required")
    return {"cart_id": cart_id, "items": [], "status": "open"}
