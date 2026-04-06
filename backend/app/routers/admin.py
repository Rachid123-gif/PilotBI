"""
Admin-only endpoints for platform management.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from supabase import Client

from app.dependencies import get_supabase_client, require_admin
from app.models.schemas import AdminMetricsResponse, AdminUserResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/admin/users", response_model=list[AdminUserResponse])
async def list_users(
    limit: int = 100,
    offset: int = 0,
    user=Depends(require_admin),
    db: Client = Depends(get_supabase_client),
):
    """List all users with organization and plan info."""
    result = (
        db.table("profiles")
        .select("id, email, full_name, organization_id, created_at, last_sign_in, organizations(name, plan)")
        .order("created_at", desc=True)
        .range(offset, offset + limit - 1)
        .execute()
    )

    users = []
    for row in result.data or []:
        org = row.get("organizations") or {}
        users.append(
            AdminUserResponse(
                id=row["id"],
                email=row.get("email", ""),
                full_name=row.get("full_name"),
                organization_id=row.get("organization_id"),
                organization_name=org.get("name"),
                plan=org.get("plan", "free"),
                created_at=row["created_at"],
                last_sign_in=row.get("last_sign_in"),
            )
        )
    return users


@router.get("/admin/metrics", response_model=AdminMetricsResponse)
async def get_metrics(
    user=Depends(require_admin),
    db: Client = Depends(get_supabase_client),
):
    """Get platform-wide metrics."""
    # Total users
    users_result = db.table("profiles").select("id", count="exact").execute()
    total_users = users_result.count or 0

    # Total organizations
    orgs_result = db.table("organizations").select("id", count="exact").execute()
    total_organizations = orgs_result.count or 0

    # Active subscriptions
    active_result = (
        db.table("organizations")
        .select("id", count="exact")
        .in_("subscription_status", ["active", "trialing"])
        .execute()
    )
    active_subscriptions = active_result.count or 0

    # Users by plan
    plans_result = db.table("organizations").select("plan").execute()
    users_by_plan: dict[str, int] = {}
    for org in plans_result.data or []:
        plan = org.get("plan", "free")
        users_by_plan[plan] = users_by_plan.get(plan, 0) + 1

    # MRR calculation (simplified: count active paid subscriptions * plan price)
    plan_prices = {"starter": 299, "pro": 599, "equipe": 999}
    mrr = 0.0
    for plan, count in users_by_plan.items():
        if plan in plan_prices:
            mrr += plan_prices[plan] * count

    # Signups last 30 days
    thirty_days_ago = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
    signups_result = (
        db.table("profiles")
        .select("id", count="exact")
        .gte("created_at", thirty_days_ago)
        .execute()
    )
    signups_last_30d = signups_result.count or 0

    # Data sources count
    ds_result = db.table("data_sources").select("id", count="exact").execute()
    data_sources_count = ds_result.count or 0

    # Reports generated
    reports_result = db.table("reports").select("id", count="exact").execute()
    reports_generated = reports_result.count or 0

    return AdminMetricsResponse(
        total_users=total_users,
        total_organizations=total_organizations,
        active_subscriptions=active_subscriptions,
        mrr=mrr,
        users_by_plan=users_by_plan,
        signups_last_30d=signups_last_30d,
        data_sources_count=data_sources_count,
        reports_generated=reports_generated,
    )
