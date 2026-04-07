"""
Dashboard endpoints - KPIs, chart data, and AI insights.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

import anthropic
from fastapi import APIRouter, Depends, HTTPException, Query

from app.config import get_settings
from app.dependencies import get_supabase_client, require_organization
from app.models.enums import KpiType, PeriodType
from app.models.schemas import ChartData, DashboardResponse, KpiData
from app.services.kpi_calculator import calculate_all_kpis, calculate_chart_data
from app.services.sector_registry import get_sector_ai_prompt, get_sector_benchmarks

logger = logging.getLogger(__name__)
router = APIRouter()


def _get_org_sector(db, org_id: str) -> Optional[str]:
    """Get the sector_slug for an organization."""
    result = db.table("organizations").select("sector_slug").eq("id", org_id).single().execute()
    return result.data.get("sector_slug") if result.data else None


@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(
    period: PeriodType = Query(PeriodType.MONTHLY, description="Aggregation period"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    user=Depends(require_organization),
    db=Depends(get_supabase_client),
):
    """Return full dashboard: KPI cards + chart data, sector-aware."""
    org_id = user["organization_id"]
    sector_slug = _get_org_sector(db, org_id)

    kpis = calculate_all_kpis(db, org_id, period, start_date, end_date, sector_slug=sector_slug)
    charts = []
    for kpi in kpis:
        chart = calculate_chart_data(db, org_id, kpi.kpi_type, period, start_date, end_date)
        if chart:
            charts.append(chart)

    return DashboardResponse(
        kpis=kpis,
        charts=charts,
        period=period,
        generated_at=datetime.now(timezone.utc),
    )


@router.get("/dashboard/kpis", response_model=list[KpiData])
async def get_kpis(
    period: PeriodType = Query(PeriodType.MONTHLY),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    user=Depends(require_organization),
    db=Depends(get_supabase_client),
):
    """Return only KPI cards data, sector-aware."""
    org_id = user["organization_id"]
    sector_slug = _get_org_sector(db, org_id)
    return calculate_all_kpis(db, org_id, period, start_date, end_date, sector_slug=sector_slug)


@router.get("/dashboard/chart/{kpi_type}", response_model=ChartData)
async def get_chart(
    kpi_type: KpiType,
    period: PeriodType = Query(PeriodType.MONTHLY),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    user=Depends(require_organization),
    db=Depends(get_supabase_client),
):
    """Return chart data for a specific KPI."""
    org_id = user["organization_id"]
    chart = calculate_chart_data(db, org_id, kpi_type, period, start_date, end_date)
    if not chart:
        raise HTTPException(status_code=404, detail=f"No data available for KPI '{kpi_type.value}'")
    return chart


@router.post("/dashboard/insights")
async def get_insights(
    user=Depends(require_organization),
    db=Depends(get_supabase_client),
):
    """
    Generate AI-powered dashboard insights (2-3 sentences).

    Cached for 1 hour to reduce API costs.
    """
    org_id = user["organization_id"]
    settings = get_settings()

    if not settings.ANTHROPIC_API_KEY:
        return {"content": None, "cached": False}

    # Check cache
    now = datetime.now(timezone.utc)
    cached = (
        db.table("dashboard_insights")
        .select("content, generated_at")
        .eq("organization_id", org_id)
        .gte("expires_at", now.isoformat())
        .order("generated_at", desc=True)
        .limit(1)
        .execute()
    )

    if cached.data:
        return {"content": cached.data[0]["content"], "cached": True}

    # Generate fresh insights
    sector_slug = _get_org_sector(db, org_id)
    kpis = calculate_all_kpis(db, org_id, PeriodType.MONTHLY, sector_slug=sector_slug)

    if not kpis:
        return {"content": None, "cached": False}

    # Build a compact KPI summary
    kpi_summary = "\n".join(
        f"- {k.label}: {k.value:,.0f} {k.unit}"
        + (f" ({'+' if k.change_pct > 0 else ''}{k.change_pct}% vs mois dernier)" if k.change_pct else "")
        for k in kpis
    )

    # Sector-specific context
    sector_context = ""
    if sector_slug:
        sector_prompt = get_sector_ai_prompt(sector_slug)
        benchmarks = get_sector_benchmarks(sector_slug)
        if sector_prompt:
            sector_context = f"\nContexte sectoriel : {sector_prompt[:200]}"
        if benchmarks:
            bench_text = ", ".join(f"{v['label']}: {v['avg']}{v['unit']}" for v in benchmarks.values())
            sector_context += f"\nBenchmarks : {bench_text}"

    prompt = f"""Analyse ces KPIs d'une PME marocaine et donne exactement 2-3 phrases percutantes en francais.
Sois direct, concret, et mentionne des chiffres. Pas de formalites.
{sector_context}

KPIs actuels :
{kpi_summary}

Reponds UNIQUEMENT avec les 2-3 phrases d'insight, rien d'autre."""

    try:
        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        content = message.content[0].text.strip()
    except Exception:
        logger.exception("Failed to generate insights")
        return {"content": None, "cached": False}

    # Cache for 1 hour
    expires_at = now + timedelta(hours=1)
    db.table("dashboard_insights").insert({
        "organization_id": org_id,
        "content": content,
        "generated_at": now.isoformat(),
        "expires_at": expires_at.isoformat(),
    }).execute()

    return {"content": content, "cached": False}
