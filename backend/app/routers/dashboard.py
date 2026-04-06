"""
Dashboard endpoints - KPIs and chart data.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.dependencies import get_supabase_client, require_organization
from app.models.enums import KpiType, PeriodType
from app.models.schemas import ChartData, DashboardResponse, KpiData
from app.services.kpi_calculator import calculate_all_kpis, calculate_chart_data

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(
    period: PeriodType = Query(PeriodType.MONTHLY, description="Aggregation period"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    user=Depends(require_organization),
    db=Depends(get_supabase_client),
):
    """Return full dashboard: KPI cards + chart data."""
    org_id = user["organization_id"]

    kpis = calculate_all_kpis(db, org_id, period, start_date, end_date)
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
    """Return only KPI cards data."""
    org_id = user["organization_id"]
    return calculate_all_kpis(db, org_id, period, start_date, end_date)


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
