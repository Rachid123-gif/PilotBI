"""
Billing endpoints - Stripe checkout, portal, subscription status.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException
from supabase import Client

from app.dependencies import get_supabase_client, require_organization
from app.models.enums import PlanTier, SubscriptionStatus
from app.models.schemas import CheckoutRequest, CheckoutResponse, PortalResponse, SubscriptionResponse
from app.services.stripe_service import create_checkout_session, create_customer, create_portal_session

logger = logging.getLogger(__name__)
router = APIRouter()


def _get_org_subscription(db: Client, org_id: str) -> dict | None:
    """Fetch organization subscription record."""
    result = (
        db.table("organizations")
        .select("stripe_customer_id, plan, subscription_status, current_period_start, current_period_end, cancel_at_period_end")
        .eq("id", org_id)
        .maybe_single()
        .execute()
    )
    return result.data


@router.get("/billing/subscription", response_model=SubscriptionResponse)
async def get_subscription(
    user=Depends(require_organization),
    db: Client = Depends(get_supabase_client),
):
    """Get current subscription status."""
    org = _get_org_subscription(db, user["organization_id"])
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    return SubscriptionResponse(
        plan=org.get("plan", PlanTier.FREE.value),
        status=org.get("subscription_status", SubscriptionStatus.ACTIVE.value),
        current_period_start=org.get("current_period_start"),
        current_period_end=org.get("current_period_end"),
        cancel_at_period_end=org.get("cancel_at_period_end", False),
        stripe_customer_id=org.get("stripe_customer_id"),
    )


@router.post("/billing/checkout", response_model=CheckoutResponse)
async def create_checkout(
    body: CheckoutRequest,
    user=Depends(require_organization),
    db: Client = Depends(get_supabase_client),
):
    """Create a Stripe Checkout session for plan upgrade."""
    org_id = user["organization_id"]

    if body.plan == PlanTier.FREE:
        raise HTTPException(status_code=400, detail="Cannot checkout for free plan")

    # Get or create Stripe customer
    org = _get_org_subscription(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    customer_id = org.get("stripe_customer_id")
    if not customer_id:
        # Fetch org name
        org_detail = db.table("organizations").select("name").eq("id", org_id).single().execute()
        org_name = org_detail.data.get("name", "Unknown")
        customer_id = create_customer(user["email"], org_name)
        db.table("organizations").update({"stripe_customer_id": customer_id}).eq("id", org_id).execute()

    session = create_checkout_session(
        customer_id=customer_id,
        plan=body.plan.value,
        interval=body.interval,
        success_url=body.success_url,
        cancel_url=body.cancel_url,
        metadata={"organization_id": org_id, "plan": body.plan.value},
    )

    return CheckoutResponse(checkout_url=session.url, session_id=session.id)


@router.post("/billing/portal", response_model=PortalResponse)
async def create_billing_portal(
    return_url: str,
    user=Depends(require_organization),
    db: Client = Depends(get_supabase_client),
):
    """Create a Stripe Customer Portal session for managing subscription."""
    org = _get_org_subscription(db, user["organization_id"])
    if not org or not org.get("stripe_customer_id"):
        raise HTTPException(status_code=400, detail="No Stripe customer found. Subscribe to a plan first.")

    session = create_portal_session(org["stripe_customer_id"], return_url)
    return PortalResponse(portal_url=session.url)
