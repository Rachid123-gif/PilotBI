"""
AI-generated reports endpoints.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from supabase import Client

from app.dependencies import get_supabase_client, require_organization
from app.models.schemas import ReportGenerateRequest, ReportList, ReportResponse
from app.services.report_generator import generate_monthly_report

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/reports", response_model=ReportList)
async def list_reports(
    user=Depends(require_organization),
    db: Client = Depends(get_supabase_client),
):
    """List all reports for the organization."""
    result = (
        db.table("reports")
        .select("*")
        .eq("organization_id", user["organization_id"])
        .order("created_at", desc=True)
        .execute()
    )
    items = result.data or []
    return ReportList(items=items, total=len(items))


@router.get("/reports/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: str,
    user=Depends(require_organization),
    db: Client = Depends(get_supabase_client),
):
    """Get a single report."""
    result = (
        db.table("reports")
        .select("*")
        .eq("id", report_id)
        .eq("organization_id", user["organization_id"])
        .maybe_single()
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="Report not found")
    return result.data


async def _generate_report_task(org_id: str, period: str, language: str, db: Client):
    """Background task to generate a report."""
    try:
        await generate_monthly_report(db, org_id, period, language)
        logger.info("Report generated for org %s, period %s", org_id, period)
    except Exception:
        logger.exception("Report generation failed for org %s, period %s", org_id, period)


@router.post("/reports/generate", status_code=status.HTTP_202_ACCEPTED)
async def trigger_report_generation(
    body: ReportGenerateRequest,
    background_tasks: BackgroundTasks,
    user=Depends(require_organization),
    db: Client = Depends(get_supabase_client),
):
    """Trigger AI report generation for a given period."""
    org_id = user["organization_id"]

    # Check if report already exists for this period
    existing = (
        db.table("reports")
        .select("id")
        .eq("organization_id", org_id)
        .eq("period", body.period)
        .maybe_single()
        .execute()
    )
    if existing.data:
        raise HTTPException(
            status_code=409,
            detail=f"Report for period '{body.period}' already exists (id: {existing.data['id']})",
        )

    background_tasks.add_task(_generate_report_task, org_id, body.period, body.language, db)
    return {"detail": "Report generation started", "period": body.period}
