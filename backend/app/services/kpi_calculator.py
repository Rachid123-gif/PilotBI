"""
KPI calculation engine.

Computes key business metrics from data_rows stored in Supabase,
with support for period-based aggregation and trend comparison.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

from supabase import Client

from app.models.enums import KpiType, PeriodType
from app.models.schemas import ChartData, ChartDataPoint, KpiData

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Label mapping for French UI
# ---------------------------------------------------------------------------
KPI_LABELS = {
    KpiType.REVENUE: ("Chiffre d'Affaires", "MAD"),
    KpiType.MARGIN: ("Marge", "MAD"),
    KpiType.CLIENT_COUNT: ("Nombre de Clients", ""),
    KpiType.ORDER_COUNT: ("Nombre de Commandes", ""),
    KpiType.AVG_ORDER_VALUE: ("Panier Moyen", "MAD"),
    KpiType.STOCK_LEVEL: ("Niveau de Stock", ""),
}


def _period_bounds(period: PeriodType, start_date: Optional[str], end_date: Optional[str]):
    """Return (current_start, current_end, previous_start, previous_end) as ISO strings."""
    now = datetime.now(timezone.utc)

    if start_date and end_date:
        current_start = datetime.fromisoformat(start_date).replace(tzinfo=timezone.utc)
        current_end = datetime.fromisoformat(end_date).replace(tzinfo=timezone.utc)
        delta = current_end - current_start
        previous_start = current_start - delta
        previous_end = current_start
    elif period == PeriodType.DAILY:
        current_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        current_end = now
        previous_start = current_start - timedelta(days=1)
        previous_end = current_start
    elif period == PeriodType.WEEKLY:
        current_start = now - timedelta(days=now.weekday())
        current_start = current_start.replace(hour=0, minute=0, second=0, microsecond=0)
        current_end = now
        previous_start = current_start - timedelta(weeks=1)
        previous_end = current_start
    else:  # MONTHLY
        current_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        current_end = now
        prev_month = current_start - timedelta(days=1)
        previous_start = prev_month.replace(day=1)
        previous_end = current_start

    return (
        current_start.isoformat(),
        current_end.isoformat(),
        previous_start.isoformat(),
        previous_end.isoformat(),
    )


def _fetch_rows(db: Client, org_id: str, date_from: str, date_to: str) -> list[dict]:
    """Fetch data_rows for an org within a date range."""
    result = (
        db.table("data_rows")
        .select("row_data, date_value")
        .eq("organization_id", org_id)
        .gte("date_value", date_from)
        .lte("date_value", date_to)
        .execute()
    )
    return result.data or []


def _safe_float(value) -> float:
    """Convert a value to float, returning 0.0 on failure."""
    if value is None:
        return 0.0
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


def _compute_kpi(rows: list[dict], kpi_type: KpiType) -> Optional[float]:
    """Compute a single KPI value from rows."""
    if not rows:
        return None

    if kpi_type == KpiType.REVENUE:
        return sum(_safe_float(r.get("row_data", {}).get("revenue")) for r in rows)

    elif kpi_type == KpiType.MARGIN:
        total_revenue = sum(_safe_float(r.get("row_data", {}).get("revenue")) for r in rows)
        total_cost = sum(_safe_float(r.get("row_data", {}).get("cost")) for r in rows)
        return total_revenue - total_cost if total_cost > 0 else None

    elif kpi_type == KpiType.CLIENT_COUNT:
        clients = set()
        for r in rows:
            client = r.get("row_data", {}).get("client_name")
            if client:
                clients.add(client)
        return float(len(clients)) if clients else None

    elif kpi_type == KpiType.ORDER_COUNT:
        invoices = set()
        for r in rows:
            inv = r.get("row_data", {}).get("invoice_id")
            if inv:
                invoices.add(inv)
        return float(len(invoices)) if invoices else float(len(rows))

    elif kpi_type == KpiType.AVG_ORDER_VALUE:
        revenues = [_safe_float(r.get("row_data", {}).get("revenue")) for r in rows if r.get("row_data", {}).get("revenue")]
        if not revenues:
            return None
        invoices = set()
        for r in rows:
            inv = r.get("row_data", {}).get("invoice_id")
            if inv:
                invoices.add(inv)
        order_count = len(invoices) if invoices else len(rows)
        return sum(revenues) / order_count if order_count > 0 else None

    elif kpi_type == KpiType.STOCK_LEVEL:
        # Use the latest stock value
        stock_values = [_safe_float(r.get("row_data", {}).get("stock_level")) for r in rows if r.get("row_data", {}).get("stock_level") is not None]
        return stock_values[-1] if stock_values else None

    return None


def calculate_all_kpis(
    db: Client,
    org_id: str,
    period: PeriodType,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> list[KpiData]:
    """
    Calculate all KPI cards for the dashboard.

    Returns a list of KpiData with current values and trend comparison.
    """
    cur_start, cur_end, prev_start, prev_end = _period_bounds(period, start_date, end_date)

    current_rows = _fetch_rows(db, org_id, cur_start, cur_end)
    previous_rows = _fetch_rows(db, org_id, prev_start, prev_end)

    kpis: list[KpiData] = []

    for kpi_type in KpiType:
        label, unit = KPI_LABELS.get(kpi_type, (kpi_type.value, ""))

        current_value = _compute_kpi(current_rows, kpi_type)
        if current_value is None:
            continue

        previous_value = _compute_kpi(previous_rows, kpi_type)

        change_pct = None
        if previous_value is not None and previous_value != 0:
            change_pct = round(((current_value - previous_value) / abs(previous_value)) * 100, 2)

        kpis.append(
            KpiData(
                kpi_type=kpi_type,
                label=label,
                value=round(current_value, 2),
                previous_value=round(previous_value, 2) if previous_value is not None else None,
                change_pct=change_pct,
                unit=unit,
                period=period,
            )
        )

    return kpis


def calculate_chart_data(
    db: Client,
    org_id: str,
    kpi_type: KpiType,
    period: PeriodType,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> Optional[ChartData]:
    """
    Build time-series chart data for a given KPI.

    Groups data by the requested period and returns data points.
    """
    now = datetime.now(timezone.utc)

    # Determine range: last 12 periods
    if start_date and end_date:
        range_start = start_date
        range_end = end_date
    elif period == PeriodType.DAILY:
        range_start = (now - timedelta(days=30)).isoformat()
        range_end = now.isoformat()
    elif period == PeriodType.WEEKLY:
        range_start = (now - timedelta(weeks=12)).isoformat()
        range_end = now.isoformat()
    else:
        range_start = (now - timedelta(days=365)).isoformat()
        range_end = now.isoformat()

    rows = _fetch_rows(db, org_id, range_start, range_end)
    if not rows:
        return None

    # Group rows by period label
    grouped: dict[str, list[dict]] = {}
    for r in rows:
        dv = r.get("date_value")
        if not dv:
            continue
        try:
            dt = datetime.fromisoformat(str(dv).replace("Z", "+00:00"))
        except (ValueError, TypeError):
            continue

        if period == PeriodType.DAILY:
            label = dt.strftime("%Y-%m-%d")
        elif period == PeriodType.WEEKLY:
            year, week, _ = dt.isocalendar()
            label = f"{year}-S{week:02d}"
        else:
            label = dt.strftime("%Y-%m")

        grouped.setdefault(label, []).append(r)

    # Compute KPI for each group
    data_points: list[ChartDataPoint] = []
    for label in sorted(grouped.keys()):
        value = _compute_kpi(grouped[label], kpi_type)
        if value is not None:
            data_points.append(ChartDataPoint(label=label, value=round(value, 2)))

    if not data_points:
        return None

    kpi_label, _ = KPI_LABELS.get(kpi_type, (kpi_type.value, ""))
    chart_type = "bar" if kpi_type in (KpiType.CLIENT_COUNT, KpiType.ORDER_COUNT, KpiType.STOCK_LEVEL) else "line"

    return ChartData(
        kpi_type=kpi_type,
        title=kpi_label,
        chart_type=chart_type,
        data_points=data_points,
        period=period,
    )
