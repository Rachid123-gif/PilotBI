"""
Stripe webhook handler.
"""

from __future__ import annotations

import logging

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request, status
from supabase import Client

from app.config import get_settings
from app.dependencies import get_supabase_client
from app.models.enums import PlanTier, SubscriptionStatus

logger = logging.getLogger(__name__)
router = APIRouter()


def _map_stripe_status(stripe_status: str) -> str:
    """Map Stripe subscription status to our enum."""
    mapping = {
        "active": SubscriptionStatus.ACTIVE.value,
        "trialing": SubscriptionStatus.TRIALING.value,
        "past_due": SubscriptionStatus.PAST_DUE.value,
        "canceled": SubscriptionStatus.CANCELED.value,
        "unpaid": SubscriptionStatus.UNPAID.value,
        "incomplete": SubscriptionStatus.INCOMPLETE.value,
        "incomplete_expired": SubscriptionStatus.CANCELED.value,
    }
    return mapping.get(stripe_status, SubscriptionStatus.ACTIVE.value)


def _resolve_plan_from_price(price_id: str) -> str:
    """Resolve a Stripe price ID to our plan tier."""
    settings = get_settings()
    price_map = settings.stripe_price_map
    for key, pid in price_map.items():
        if pid == price_id:
            plan = key.rsplit("_", 1)[0]  # e.g. "starter_monthly" -> "starter"
            return plan
    return PlanTier.FREE.value


@router.post("/webhooks/stripe", status_code=status.HTTP_200_OK)
async def stripe_webhook(
    request: Request,
    db: Client = Depends(get_supabase_client),
):
    """Handle Stripe webhook events with signature verification."""
    settings = get_settings()
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not sig_header:
        raise HTTPException(status_code=400, detail="Missing Stripe signature")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET,
        )
    except stripe.error.SignatureVerificationError:
        logger.warning("Stripe webhook signature verification failed")
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as exc:
        logger.exception("Stripe webhook error")
        raise HTTPException(status_code=400, detail=str(exc))

    event_type = event["type"]
    data_object = event["data"]["object"]
    logger.info("Stripe webhook received: %s", event_type)

    # --- checkout.session.completed ---
    if event_type == "checkout.session.completed":
        _handle_checkout_completed(db, data_object)

    # --- customer.subscription.created / updated ---
    elif event_type in ("customer.subscription.created", "customer.subscription.updated"):
        _handle_subscription_update(db, data_object)

    # --- customer.subscription.deleted ---
    elif event_type == "customer.subscription.deleted":
        _handle_subscription_deleted(db, data_object)

    # --- invoice.payment_failed ---
    elif event_type == "invoice.payment_failed":
        _handle_payment_failed(db, data_object)

    return {"received": True}


def _handle_checkout_completed(db: Client, session: dict):
    """Process a completed checkout session."""
    customer_id = session.get("customer")
    metadata = session.get("metadata", {})
    org_id = metadata.get("organization_id")
    plan = metadata.get("plan", PlanTier.FREE.value)

    if not org_id:
        logger.warning("Checkout completed but no organization_id in metadata")
        return

    db.table("organizations").update({
        "stripe_customer_id": customer_id,
        "plan": plan,
        "subscription_status": SubscriptionStatus.ACTIVE.value,
    }).eq("id", org_id).execute()

    logger.info("Checkout completed for org %s, plan %s", org_id, plan)


def _handle_subscription_update(db: Client, subscription: dict):
    """Process a subscription create or update."""
    customer_id = subscription.get("customer")
    stripe_status = subscription.get("status", "active")
    cancel_at_period_end = subscription.get("cancel_at_period_end", False)

    # Extract plan from line items
    items = subscription.get("items", {}).get("data", [])
    plan = PlanTier.FREE.value
    if items:
        price_id = items[0].get("price", {}).get("id", "")
        plan = _resolve_plan_from_price(price_id)

    current_period_start = subscription.get("current_period_start")
    current_period_end = subscription.get("current_period_end")

    # Find organization by stripe_customer_id
    result = (
        db.table("organizations")
        .select("id")
        .eq("stripe_customer_id", customer_id)
        .maybe_single()
        .execute()
    )
    if not result.data:
        logger.warning("No organization found for Stripe customer %s", customer_id)
        return

    from datetime import datetime, timezone

    update_data = {
        "plan": plan,
        "subscription_status": _map_stripe_status(stripe_status),
        "cancel_at_period_end": cancel_at_period_end,
    }
    if current_period_start:
        update_data["current_period_start"] = datetime.fromtimestamp(
            current_period_start, tz=timezone.utc
        ).isoformat()
    if current_period_end:
        update_data["current_period_end"] = datetime.fromtimestamp(
            current_period_end, tz=timezone.utc
        ).isoformat()

    db.table("organizations").update(update_data).eq("id", result.data["id"]).execute()
    logger.info("Subscription updated for org %s: plan=%s status=%s", result.data["id"], plan, stripe_status)


def _handle_subscription_deleted(db: Client, subscription: dict):
    """Process a subscription cancellation."""
    customer_id = subscription.get("customer")

    result = (
        db.table("organizations")
        .select("id")
        .eq("stripe_customer_id", customer_id)
        .maybe_single()
        .execute()
    )
    if not result.data:
        return

    db.table("organizations").update({
        "plan": PlanTier.FREE.value,
        "subscription_status": SubscriptionStatus.CANCELED.value,
        "cancel_at_period_end": False,
    }).eq("id", result.data["id"]).execute()

    logger.info("Subscription deleted for org %s, reverted to free", result.data["id"])


def _handle_payment_failed(db: Client, invoice: dict):
    """Log a failed payment attempt."""
    customer_id = invoice.get("customer")
    logger.warning("Payment failed for Stripe customer %s", customer_id)

    result = (
        db.table("organizations")
        .select("id")
        .eq("stripe_customer_id", customer_id)
        .maybe_single()
        .execute()
    )
    if result.data:
        db.table("organizations").update({
            "subscription_status": SubscriptionStatus.PAST_DUE.value,
        }).eq("id", result.data["id"]).execute()
