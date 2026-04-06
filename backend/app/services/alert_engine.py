"""
Alert evaluation engine.

Evaluates configured alerts against current KPI values and triggers
notifications when conditions are met, with 24-hour rate limiting.
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from supabase import Client

from app.models.enums import AlertCondition, KpiType, PeriodType
from app.services.kpi_calculator import calculate_all_kpis
from app.services.notification import notify_alert

logger = logging.getLogger(__name__)

RATE_LIMIT_HOURS = 24


def _get_active_alerts(db: Client, org_id: str) -> List[Dict[str, Any]]:
    """Fetch all active alerts for the organization."""
    result = (
        db.table("alerts")
        .select("*")
        .eq("organization_id", org_id)
        .eq("is_active", True)
        .execute()
    )
    return result.data or []


def _is_rate_limited(alert: Dict[str, Any]) -> bool:
    """Check if the alert was triggered within the rate limit window."""
    last_triggered = alert.get("last_triggered_at")
    if not last_triggered:
        return False

    try:
        last_dt = datetime.fromisoformat(str(last_triggered).replace("Z", "+00:00"))
        cutoff = datetime.now(timezone.utc) - timedelta(hours=RATE_LIMIT_HOURS)
        return last_dt > cutoff
    except (ValueError, TypeError):
        return False


def _check_condition(
    condition: str,
    threshold: float,
    current_value: float,
    previous_value: Optional[float],
) -> bool:
    """
    Evaluate an alert condition.

    - ABOVE: current_value > threshold
    - BELOW: current_value < threshold
    - CHANGE_PCT: percent change from previous exceeds threshold (absolute)
    """
    if condition == AlertCondition.ABOVE.value:
        return current_value > threshold

    elif condition == AlertCondition.BELOW.value:
        return current_value < threshold

    elif condition == AlertCondition.CHANGE_PCT.value:
        if previous_value is None or previous_value == 0:
            return False
        change_pct = ((current_value - previous_value) / abs(previous_value)) * 100
        return abs(change_pct) > abs(threshold)

    return False


def _record_trigger(
    db: Client,
    alert: Dict[str, Any],
    actual_value: float,
    org_id: str,
) -> str:
    """Record an alert trigger in the history and update last_triggered_at."""
    now = datetime.now(timezone.utc).isoformat()
    history_id = str(uuid.uuid4())

    db.table("alert_history").insert({
        "id": history_id,
        "alert_id": alert["id"],
        "organization_id": org_id,
        "actual_value": actual_value,
        "triggered_at": now,
        "notified": False,
    }).execute()

    db.table("alerts").update({
        "last_triggered_at": now,
    }).eq("id", alert["id"]).execute()

    return history_id


async def evaluate_alerts(db: Client, org_id: str) -> List[Dict[str, Any]]:
    """
    Evaluate all active alerts for an organization.

    1. Fetch current KPI values.
    2. For each active alert, check if the condition is met.
    3. If triggered and not rate-limited, record and send notifications.

    Returns a list of triggered alert records.
    """
    alerts = _get_active_alerts(db, org_id)
    if not alerts:
        return []

    # Calculate current KPIs
    kpis = calculate_all_kpis(db, org_id, PeriodType.MONTHLY)
    kpi_map: Dict[str, Any] = {}
    for kpi in kpis:
        kpi_map[kpi.kpi_type.value] = kpi

    triggered: List[Dict[str, Any]] = []

    for alert in alerts:
        kpi_type = alert.get("kpi_type")
        kpi = kpi_map.get(kpi_type)

        if not kpi:
            logger.debug("No KPI data for alert %s (type=%s)", alert["id"], kpi_type)
            continue

        # Check rate limiting
        if _is_rate_limited(alert):
            logger.debug("Alert %s is rate-limited, skipping", alert["id"])
            continue

        # Check condition
        condition_met = _check_condition(
            condition=alert["condition"],
            threshold=alert["threshold"],
            current_value=kpi.value,
            previous_value=kpi.previous_value,
        )

        if not condition_met:
            continue

        # Record trigger
        history_id = _record_trigger(db, alert, kpi.value, org_id)

        # Send notifications
        notified = False
        try:
            await notify_alert(db, alert, kpi.value)
            notified = True
        except Exception:
            logger.exception("Failed to send notification for alert %s", alert["id"])

        # Update notification status
        db.table("alert_history").update({"notified": notified}).eq("id", history_id).execute()

        triggered.append({
            "alert_id": alert["id"],
            "alert_name": alert["name"],
            "kpi_type": kpi_type,
            "condition": alert["condition"],
            "threshold": alert["threshold"],
            "actual_value": kpi.value,
            "notified": notified,
        })

        logger.info(
            "Alert triggered: '%s' (%s %s %.2f, actual=%.2f)",
            alert["name"], kpi_type, alert["condition"], alert["threshold"], kpi.value,
        )

    return triggered
