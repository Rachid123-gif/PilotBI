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
    # Core
    KpiType.REVENUE: ("Chiffre d'Affaires", "MAD"),
    KpiType.MARGIN: ("Marge", "MAD"),
    KpiType.CLIENT_COUNT: ("Nombre de Clients", ""),
    KpiType.ORDER_COUNT: ("Nombre de Commandes", ""),
    KpiType.AVG_ORDER_VALUE: ("Panier Moyen", "MAD"),
    KpiType.STOCK_LEVEL: ("Niveau de Stock", ""),
    # Distribution
    KpiType.RECEIVABLES: ("Creances Clients", "MAD"),
    KpiType.REVENUE_PER_REP: ("CA par Commercial", "MAD"),
    KpiType.STOCK_ROTATION: ("Rotation Stock", "x"),
    KpiType.RETURN_RATE: ("Taux de Retour", "%"),
    # Retail
    KpiType.REVENUE_PER_STORE: ("CA par Magasin", "MAD"),
    KpiType.CONVERSION_RATE: ("Taux de Conversion", "%"),
    # Industrie
    KpiType.PRODUCTION_COST: ("Cout de Production", "MAD"),
    KpiType.YIELD_RATE: ("Rendement", "%"),
    KpiType.DEFECT_RATE: ("Taux de Rebut", "%"),
    KpiType.ON_TIME_DELIVERY: ("Livraison a Temps", "%"),
    # Transport
    KpiType.COST_PER_KM: ("Cout par km", "MAD"),
    KpiType.FILL_RATE: ("Taux de Remplissage", "%"),
    KpiType.FUEL_CONSUMPTION: ("Consommation Carburant", "L"),
    KpiType.DELIVERIES_COUNT: ("Nombre de Livraisons", ""),
    # Restaurant
    KpiType.FOOD_COST_PCT: ("Food Cost", "%"),
    KpiType.DISHES_SOLD: ("Plats Vendus", ""),
    KpiType.WASTE_RATE: ("Taux de Gaspillage", "%"),
    # E-commerce
    KpiType.CAC: ("Cout d'Acquisition", "MAD"),
    KpiType.LTV: ("Valeur Vie Client", "MAD"),
    KpiType.RETURN_RATE_ECOM: ("Taux de Retour", "%"),
    KpiType.REVENUE_PER_CHANNEL: ("CA par Canal", "MAD"),
    # Clinique
    KpiType.REVENUE_PER_DOCTOR: ("CA par Medecin", "MAD"),
    KpiType.PATIENT_COUNT: ("Nombre de Patients", ""),
    KpiType.OCCUPANCY_RATE: ("Taux d'Occupation", "%"),
    # Pharmacie
    KpiType.REVENUE_PER_STORE_PHARMA: ("CA par Officine", "MAD"),
    KpiType.PRESCRIPTIONS_PER_DAY: ("Ordonnances/Jour", ""),
    KpiType.CRITICAL_STOCK: ("Ruptures de Stock", ""),
    # Immobilier
    KpiType.SALES_COUNT: ("Nombre de Ventes", ""),
    KpiType.COMMERCIALIZATION_RATE: ("Taux Commercialisation", "%"),
    KpiType.PRICE_PER_SQM: ("Prix au m2", "MAD"),
    KpiType.AVG_SALE_DELAY: ("Delai Moyen Vente", "jours"),
    # Hotel
    KpiType.REVPAR: ("RevPAR", "MAD"),
    KpiType.ADR: ("Tarif Moyen/Nuit", "MAD"),
    KpiType.OCCUPANCY_RATE_HOTEL: ("Taux d'Occupation", "%"),
    KpiType.FB_REVENUE: ("CA Restauration", "MAD"),
    # Services
    KpiType.BILLABLE_HOURS: ("Heures Facturees", "h"),
    KpiType.COLLECTION_RATE: ("Taux de Recouvrement", "%"),
    KpiType.ACTIVE_CONTRACTS: ("Contrats Actifs", ""),
    KpiType.MARGIN_PER_PROJECT: ("Marge par Projet", "MAD"),
    # Agriculture
    KpiType.YIELD_PER_HA: ("Rendement/ha", "T"),
    KpiType.COST_PER_TON: ("Cout par Tonne", "MAD"),
    KpiType.HARVEST_STOCK: ("Stock Recolte", "T"),
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
        stock_values = [_safe_float(r.get("row_data", {}).get("stock_level")) for r in rows if r.get("row_data", {}).get("stock_level") is not None]
        return stock_values[-1] if stock_values else None

    # ── Distribution ──
    elif kpi_type == KpiType.RECEIVABLES:
        return sum(_safe_float(r.get("row_data", {}).get("receivables") or r.get("row_data", {}).get("amount_ttc", 0)) for r in rows if r.get("row_data", {}).get("receivables") is not None)

    elif kpi_type == KpiType.REVENUE_PER_REP:
        reps = {}
        for r in rows:
            rep = r.get("row_data", {}).get("sales_rep")
            if rep:
                reps.setdefault(rep, 0.0)
                reps[rep] += _safe_float(r.get("row_data", {}).get("revenue"))
        return sum(reps.values()) / len(reps) if reps else None

    elif kpi_type == KpiType.STOCK_ROTATION:
        total_sold = sum(_safe_float(r.get("row_data", {}).get("quantity")) for r in rows)
        stock_vals = [_safe_float(r.get("row_data", {}).get("stock_level")) for r in rows if r.get("row_data", {}).get("stock_level") is not None]
        avg_stock = sum(stock_vals) / len(stock_vals) if stock_vals else 0
        return round(total_sold / avg_stock, 2) if avg_stock > 0 else None

    elif kpi_type == KpiType.RETURN_RATE:
        total_orders = len(rows)
        returns = sum(1 for r in rows if r.get("row_data", {}).get("return") or r.get("row_data", {}).get("retour"))
        return round((returns / total_orders) * 100, 2) if total_orders > 0 else None

    # ── Retail ──
    elif kpi_type == KpiType.REVENUE_PER_STORE:
        stores = {}
        for r in rows:
            store = r.get("row_data", {}).get("store_id")
            if store:
                stores.setdefault(store, 0.0)
                stores[store] += _safe_float(r.get("row_data", {}).get("revenue"))
        return sum(stores.values()) / len(stores) if stores else None

    elif kpi_type == KpiType.CONVERSION_RATE:
        total_visits = sum(_safe_float(r.get("row_data", {}).get("visits", 0)) for r in rows)
        total_orders = len({r.get("row_data", {}).get("invoice_id") for r in rows if r.get("row_data", {}).get("invoice_id")}) or len(rows)
        return round((total_orders / total_visits) * 100, 2) if total_visits > 0 else None

    # ── Industrie ──
    elif kpi_type == KpiType.PRODUCTION_COST:
        return sum(_safe_float(r.get("row_data", {}).get("cost")) for r in rows)

    elif kpi_type == KpiType.YIELD_RATE:
        total_produced = sum(_safe_float(r.get("row_data", {}).get("quantity")) for r in rows)
        total_input = sum(_safe_float(r.get("row_data", {}).get("input_quantity", 0)) for r in rows)
        return round((total_produced / total_input) * 100, 2) if total_input > 0 else None

    elif kpi_type == KpiType.DEFECT_RATE:
        total = sum(_safe_float(r.get("row_data", {}).get("quantity")) for r in rows)
        defects = sum(_safe_float(r.get("row_data", {}).get("defect_quantity", 0)) for r in rows)
        return round((defects / total) * 100, 2) if total > 0 else None

    elif kpi_type == KpiType.ON_TIME_DELIVERY:
        total = len(rows)
        on_time = sum(1 for r in rows if r.get("row_data", {}).get("on_time") in (True, "oui", "1", 1))
        return round((on_time / total) * 100, 2) if total > 0 else None

    # ── Transport ──
    elif kpi_type == KpiType.COST_PER_KM:
        total_cost = sum(_safe_float(r.get("row_data", {}).get("cost")) for r in rows)
        total_km = sum(_safe_float(r.get("row_data", {}).get("distance")) for r in rows)
        return round(total_cost / total_km, 2) if total_km > 0 else None

    elif kpi_type == KpiType.FILL_RATE:
        rates = [_safe_float(r.get("row_data", {}).get("fill_rate", 0)) for r in rows if r.get("row_data", {}).get("fill_rate") is not None]
        return round(sum(rates) / len(rates), 2) if rates else None

    elif kpi_type == KpiType.FUEL_CONSUMPTION:
        return sum(_safe_float(r.get("row_data", {}).get("fuel")) for r in rows)

    elif kpi_type == KpiType.DELIVERIES_COUNT:
        deliveries = {r.get("row_data", {}).get("delivery_id") for r in rows if r.get("row_data", {}).get("delivery_id")}
        return float(len(deliveries)) if deliveries else float(len(rows))

    # ── Restaurant ──
    elif kpi_type == KpiType.FOOD_COST_PCT:
        total_rev = sum(_safe_float(r.get("row_data", {}).get("revenue")) for r in rows)
        total_cost = sum(_safe_float(r.get("row_data", {}).get("cost")) for r in rows)
        return round((total_cost / total_rev) * 100, 2) if total_rev > 0 else None

    elif kpi_type == KpiType.DISHES_SOLD:
        return sum(_safe_float(r.get("row_data", {}).get("quantity", 1)) for r in rows)

    elif kpi_type == KpiType.WASTE_RATE:
        total = sum(_safe_float(r.get("row_data", {}).get("quantity", 0)) for r in rows)
        waste = sum(_safe_float(r.get("row_data", {}).get("waste", 0)) for r in rows)
        return round((waste / total) * 100, 2) if total > 0 else None

    # ── E-commerce ──
    elif kpi_type == KpiType.CAC:
        total_cost = sum(_safe_float(r.get("row_data", {}).get("marketing_cost", 0)) for r in rows)
        new_clients = len({r.get("row_data", {}).get("client_name") for r in rows if r.get("row_data", {}).get("client_name")})
        return round(total_cost / new_clients, 2) if new_clients > 0 else None

    elif kpi_type == KpiType.LTV:
        clients = {}
        for r in rows:
            c = r.get("row_data", {}).get("client_name")
            if c:
                clients.setdefault(c, 0.0)
                clients[c] += _safe_float(r.get("row_data", {}).get("revenue"))
        return round(sum(clients.values()) / len(clients), 2) if clients else None

    elif kpi_type == KpiType.RETURN_RATE_ECOM:
        total = len(rows)
        returns = sum(1 for r in rows if r.get("row_data", {}).get("returned") in (True, "oui", "1", 1))
        return round((returns / total) * 100, 2) if total > 0 else None

    elif kpi_type == KpiType.REVENUE_PER_CHANNEL:
        channels = {}
        for r in rows:
            ch = r.get("row_data", {}).get("channel")
            if ch:
                channels.setdefault(ch, 0.0)
                channels[ch] += _safe_float(r.get("row_data", {}).get("revenue"))
        return sum(channels.values()) / len(channels) if channels else None

    # ── Clinique ──
    elif kpi_type == KpiType.REVENUE_PER_DOCTOR:
        doctors = {}
        for r in rows:
            doc = r.get("row_data", {}).get("doctor_name")
            if doc:
                doctors.setdefault(doc, 0.0)
                doctors[doc] += _safe_float(r.get("row_data", {}).get("revenue"))
        return sum(doctors.values()) / len(doctors) if doctors else None

    elif kpi_type == KpiType.PATIENT_COUNT:
        patients = {r.get("row_data", {}).get("patient_name") for r in rows if r.get("row_data", {}).get("patient_name")}
        return float(len(patients)) if patients else None

    elif kpi_type == KpiType.OCCUPANCY_RATE:
        occupied = sum(_safe_float(r.get("row_data", {}).get("occupied", 0)) for r in rows)
        capacity = sum(_safe_float(r.get("row_data", {}).get("capacity", 0)) for r in rows)
        return round((occupied / capacity) * 100, 2) if capacity > 0 else None

    # ── Pharmacie ──
    elif kpi_type == KpiType.REVENUE_PER_STORE_PHARMA:
        stores = {}
        for r in rows:
            s = r.get("row_data", {}).get("store_id")
            if s:
                stores.setdefault(s, 0.0)
                stores[s] += _safe_float(r.get("row_data", {}).get("revenue"))
        return sum(stores.values()) / len(stores) if stores else None

    elif kpi_type == KpiType.PRESCRIPTIONS_PER_DAY:
        prescriptions = {r.get("row_data", {}).get("prescription_id") for r in rows if r.get("row_data", {}).get("prescription_id")}
        dates = {r.get("date_value") for r in rows if r.get("date_value")}
        n_days = max(len(dates), 1)
        return round(len(prescriptions) / n_days, 1) if prescriptions else None

    elif kpi_type == KpiType.CRITICAL_STOCK:
        return sum(1 for r in rows if _safe_float(r.get("row_data", {}).get("stock_level", 999)) < 5)

    # ── Immobilier ──
    elif kpi_type == KpiType.SALES_COUNT:
        sales = {r.get("row_data", {}).get("unit_id") or r.get("row_data", {}).get("invoice_id") for r in rows if r.get("row_data", {}).get("unit_id") or r.get("row_data", {}).get("invoice_id")}
        return float(len(sales)) if sales else float(len(rows))

    elif kpi_type == KpiType.COMMERCIALIZATION_RATE:
        sold = len({r.get("row_data", {}).get("unit_id") for r in rows if r.get("row_data", {}).get("unit_id")})
        total = sum(_safe_float(r.get("row_data", {}).get("total_units", 0)) for r in rows[:1])
        return round((sold / total) * 100, 2) if total > 0 else None

    elif kpi_type == KpiType.PRICE_PER_SQM:
        total_rev = sum(_safe_float(r.get("row_data", {}).get("revenue")) for r in rows)
        total_sqm = sum(_safe_float(r.get("row_data", {}).get("area_sqm")) for r in rows)
        return round(total_rev / total_sqm, 2) if total_sqm > 0 else None

    elif kpi_type == KpiType.AVG_SALE_DELAY:
        delays = [_safe_float(r.get("row_data", {}).get("sale_delay", 0)) for r in rows if r.get("row_data", {}).get("sale_delay") is not None]
        return round(sum(delays) / len(delays), 1) if delays else None

    # ── Hotel ──
    elif kpi_type == KpiType.REVPAR:
        total_rev = sum(_safe_float(r.get("row_data", {}).get("revenue")) for r in rows)
        room_nights = sum(_safe_float(r.get("row_data", {}).get("nights", 1)) for r in rows)
        return round(total_rev / room_nights, 2) if room_nights > 0 else None

    elif kpi_type == KpiType.ADR:
        total_rev = sum(_safe_float(r.get("row_data", {}).get("room_rate") or r.get("row_data", {}).get("revenue", 0)) for r in rows)
        occupied_rooms = len(rows)
        return round(total_rev / occupied_rooms, 2) if occupied_rooms > 0 else None

    elif kpi_type == KpiType.OCCUPANCY_RATE_HOTEL:
        nights_sold = sum(_safe_float(r.get("row_data", {}).get("nights", 1)) for r in rows)
        capacity = sum(_safe_float(r.get("row_data", {}).get("capacity", 0)) for r in rows[:1])
        dates = {r.get("date_value") for r in rows if r.get("date_value")}
        n_days = max(len(dates), 1)
        total_available = capacity * n_days if capacity > 0 else nights_sold * 2
        return round((nights_sold / total_available) * 100, 2) if total_available > 0 else None

    elif kpi_type == KpiType.FB_REVENUE:
        return sum(_safe_float(r.get("row_data", {}).get("fb_revenue") or 0) for r in rows)

    # ── Services B2B ──
    elif kpi_type == KpiType.BILLABLE_HOURS:
        return sum(_safe_float(r.get("row_data", {}).get("billable_hours") or r.get("row_data", {}).get("hours", 0)) for r in rows)

    elif kpi_type == KpiType.COLLECTION_RATE:
        collected = sum(_safe_float(r.get("row_data", {}).get("amount_collected", 0)) for r in rows)
        invoiced = sum(_safe_float(r.get("row_data", {}).get("amount_invoiced") or r.get("row_data", {}).get("revenue", 0)) for r in rows)
        return round((collected / invoiced) * 100, 2) if invoiced > 0 else None

    elif kpi_type == KpiType.ACTIVE_CONTRACTS:
        contracts = {r.get("row_data", {}).get("contract_id") for r in rows if r.get("row_data", {}).get("contract_id")}
        return float(len(contracts)) if contracts else None

    elif kpi_type == KpiType.MARGIN_PER_PROJECT:
        projects = {}
        for r in rows:
            p = r.get("row_data", {}).get("project_name")
            if p:
                projects.setdefault(p, {"rev": 0.0, "cost": 0.0})
                projects[p]["rev"] += _safe_float(r.get("row_data", {}).get("revenue"))
                projects[p]["cost"] += _safe_float(r.get("row_data", {}).get("cost"))
        if not projects:
            return None
        margins = [p["rev"] - p["cost"] for p in projects.values()]
        return round(sum(margins) / len(margins), 2)

    # ── Agriculture ──
    elif kpi_type == KpiType.YIELD_PER_HA:
        total_harvest = sum(_safe_float(r.get("row_data", {}).get("harvest")) for r in rows)
        total_ha = sum(_safe_float(r.get("row_data", {}).get("area_ha")) for r in rows)
        return round(total_harvest / total_ha, 2) if total_ha > 0 else None

    elif kpi_type == KpiType.COST_PER_TON:
        total_cost = sum(_safe_float(r.get("row_data", {}).get("cost")) for r in rows)
        total_harvest = sum(_safe_float(r.get("row_data", {}).get("harvest")) for r in rows)
        return round(total_cost / total_harvest, 2) if total_harvest > 0 else None

    elif kpi_type == KpiType.HARVEST_STOCK:
        vals = [_safe_float(r.get("row_data", {}).get("harvest")) for r in rows if r.get("row_data", {}).get("harvest") is not None]
        return vals[-1] if vals else None

    return None


def calculate_all_kpis(
    db: Client,
    org_id: str,
    period: PeriodType,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    sector_slug: Optional[str] = None,
) -> list[KpiData]:
    """
    Calculate KPI cards for the dashboard.

    If sector_slug is provided, only compute KPIs relevant to that sector.
    Otherwise, compute the 6 core KPIs.
    """
    from app.services.sector_registry import get_sector_kpis

    cur_start, cur_end, prev_start, prev_end = _period_bounds(period, start_date, end_date)

    current_rows = _fetch_rows(db, org_id, cur_start, cur_end)
    previous_rows = _fetch_rows(db, org_id, prev_start, prev_end)

    # Determine which KPIs to calculate
    if sector_slug:
        kpi_slugs = get_sector_kpis(sector_slug)
    else:
        kpi_slugs = ["revenue", "margin", "client_count", "order_count", "avg_order_value", "stock_level"]

    kpis: list[KpiData] = []

    for slug in kpi_slugs:
        try:
            kpi_type = KpiType(slug)
        except ValueError:
            continue

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
