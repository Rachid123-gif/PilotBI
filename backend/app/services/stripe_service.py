"""
Stripe integration service.

Handles customer creation, checkout sessions, and billing portal.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

import stripe

from app.config import get_settings

logger = logging.getLogger(__name__)


def _init_stripe() -> None:
    """Set the Stripe API key."""
    settings = get_settings()
    stripe.api_key = settings.STRIPE_SECRET_KEY


def create_customer(email: str, org_name: str) -> str:
    """
    Create a Stripe customer.

    Returns the Stripe customer ID.
    """
    _init_stripe()
    customer = stripe.Customer.create(
        email=email,
        name=org_name,
        metadata={"source": "pilotbi"},
    )
    logger.info("Created Stripe customer %s for %s", customer.id, email)
    return customer.id


def create_checkout_session(
    customer_id: str,
    plan: str,
    interval: str,
    success_url: str,
    cancel_url: str,
    metadata: Optional[Dict[str, str]] = None,
) -> Any:
    """
    Create a Stripe Checkout session for a subscription.

    Parameters
    ----------
    customer_id : str
        Stripe customer ID.
    plan : str
        Plan name (starter, pro, equipe).
    interval : str
        Billing interval (monthly, annual).
    success_url : str
        URL to redirect on success.
    cancel_url : str
        URL to redirect on cancel.
    metadata : dict, optional
        Additional metadata for the session.

    Returns
    -------
    stripe.checkout.Session
    """
    _init_stripe()
    settings = get_settings()

    price_key = f"{plan}_{interval}"
    price_id = settings.stripe_price_map.get(price_key)

    if not price_id:
        raise ValueError(f"No Stripe price configured for plan '{plan}' with interval '{interval}'")

    session = stripe.checkout.Session.create(
        customer=customer_id,
        mode="subscription",
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=cancel_url,
        metadata=metadata or {},
        allow_promotion_codes=True,
        billing_address_collection="auto",
        locale="fr",
    )

    logger.info("Created checkout session %s for customer %s (plan=%s)", session.id, customer_id, price_key)
    return session


def create_portal_session(customer_id: str, return_url: str) -> Any:
    """
    Create a Stripe Customer Portal session for managing subscriptions.

    Returns a stripe.billing_portal.Session.
    """
    _init_stripe()

    session = stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url=return_url,
    )

    logger.info("Created portal session for customer %s", customer_id)
    return session


def get_subscription(customer_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve the active subscription for a customer.

    Returns subscription data dict or None.
    """
    _init_stripe()

    subscriptions = stripe.Subscription.list(
        customer=customer_id,
        status="all",
        limit=1,
    )

    if subscriptions.data:
        sub = subscriptions.data[0]
        return {
            "id": sub.id,
            "status": sub.status,
            "plan": sub.items.data[0].price.id if sub.items.data else None,
            "current_period_start": sub.current_period_start,
            "current_period_end": sub.current_period_end,
            "cancel_at_period_end": sub.cancel_at_period_end,
        }

    return None


def cancel_subscription(subscription_id: str, at_period_end: bool = True) -> Any:
    """
    Cancel a subscription.

    Parameters
    ----------
    subscription_id : str
        Stripe subscription ID.
    at_period_end : bool
        If True, cancel at the end of the billing period.
        If False, cancel immediately.
    """
    _init_stripe()

    if at_period_end:
        sub = stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=True,
        )
    else:
        sub = stripe.Subscription.cancel(subscription_id)

    logger.info("Cancelled subscription %s (at_period_end=%s)", subscription_id, at_period_end)
    return sub
