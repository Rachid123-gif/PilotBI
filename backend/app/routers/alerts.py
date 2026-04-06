"""
Alert CRUD and history endpoints.
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client

from app.dependencies import get_supabase_client, require_organization
from app.models.schemas import AlertCreate, AlertHistoryResponse, AlertResponse, AlertUpdate

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/alerts", response_model=list[AlertResponse])
async def list_alerts(
    user=Depends(require_organization),
    db: Client = Depends(get_supabase_client),
):
    """List all alerts for the organization."""
    result = (
        db.table("alerts")
        .select("*")
        .eq("organization_id", user["organization_id"])
        .order("created_at", desc=True)
        .execute()
    )
    return result.data or []


@router.get("/alerts/history", response_model=list[AlertHistoryResponse])
async def alert_history(
    limit: int = 50,
    user=Depends(require_organization),
    db: Client = Depends(get_supabase_client),
):
    """Get alert trigger history for the organization."""
    result = (
        db.table("alert_history")
        .select("*, alerts(name, kpi_type, condition, threshold)")
        .eq("organization_id", user["organization_id"])
        .order("triggered_at", desc=True)
        .limit(limit)
        .execute()
    )
    items = []
    for row in result.data or []:
        alert_data = row.get("alerts", {}) or {}
        items.append(
            AlertHistoryResponse(
                id=row["id"],
                alert_id=row["alert_id"],
                alert_name=alert_data.get("name", "Unknown"),
                kpi_type=alert_data.get("kpi_type", "revenue"),
                condition=alert_data.get("condition", "above"),
                threshold=alert_data.get("threshold", 0),
                actual_value=row["actual_value"],
                triggered_at=row["triggered_at"],
                notified=row.get("notified", False),
            )
        )
    return items


@router.get("/alerts/{alert_id}", response_model=AlertResponse)
async def get_alert(
    alert_id: str,
    user=Depends(require_organization),
    db: Client = Depends(get_supabase_client),
):
    """Get a single alert."""
    result = (
        db.table("alerts")
        .select("*")
        .eq("id", alert_id)
        .eq("organization_id", user["organization_id"])
        .maybe_single()
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="Alert not found")
    return result.data


@router.post("/alerts", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
async def create_alert(
    body: AlertCreate,
    user=Depends(require_organization),
    db: Client = Depends(get_supabase_client),
):
    """Create a new alert."""
    now = datetime.now(timezone.utc).isoformat()
    alert_id = str(uuid.uuid4())

    data = {
        "id": alert_id,
        "organization_id": user["organization_id"],
        "created_by": user["id"],
        "name": body.name,
        "kpi_type": body.kpi_type.value,
        "condition": body.condition.value,
        "threshold": body.threshold,
        "notify_email": body.notify_email,
        "notify_whatsapp": body.notify_whatsapp,
        "is_active": body.is_active,
        "created_at": now,
        "updated_at": now,
    }

    result = db.table("alerts").insert(data).execute()
    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to create alert")
    return result.data[0]


@router.put("/alerts/{alert_id}", response_model=AlertResponse)
async def update_alert(
    alert_id: str,
    body: AlertUpdate,
    user=Depends(require_organization),
    db: Client = Depends(get_supabase_client),
):
    """Update an existing alert."""
    # Verify ownership
    existing = (
        db.table("alerts")
        .select("id")
        .eq("id", alert_id)
        .eq("organization_id", user["organization_id"])
        .maybe_single()
        .execute()
    )
    if not existing.data:
        raise HTTPException(status_code=404, detail="Alert not found")

    update_data = body.model_dump(exclude_none=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    # Convert enums to values
    for key in ("kpi_type", "condition"):
        if key in update_data and hasattr(update_data[key], "value"):
            update_data[key] = update_data[key].value

    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()

    result = db.table("alerts").update(update_data).eq("id", alert_id).execute()
    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to update alert")
    return result.data[0]


@router.delete("/alerts/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_alert(
    alert_id: str,
    user=Depends(require_organization),
    db: Client = Depends(get_supabase_client),
):
    """Delete an alert."""
    existing = (
        db.table("alerts")
        .select("id")
        .eq("id", alert_id)
        .eq("organization_id", user["organization_id"])
        .maybe_single()
        .execute()
    )
    if not existing.data:
        raise HTTPException(status_code=404, detail="Alert not found")

    # Delete history first
    db.table("alert_history").delete().eq("alert_id", alert_id).execute()
    db.table("alerts").delete().eq("id", alert_id).execute()
