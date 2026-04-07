"""
Dashboard configuration builder.

Builds a sector-specific dashboard layout based on the organization's
sector and available data columns.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from supabase import Client

from app.models.enums import KpiType
from app.services.sector_registry import (
    get_sector,
    get_sector_default_alerts,
    get_sector_primary_kpis,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# KPI display config (icon + color for every KPI type)
# ---------------------------------------------------------------------------
KPI_DISPLAY: Dict[str, Dict[str, str]] = {
    # Core
    "revenue": {"icon": "trending-up", "color": "#2563EB"},
    "margin": {"icon": "bar-chart-2", "color": "#10B981"},
    "client_count": {"icon": "users", "color": "#8B5CF6"},
    "order_count": {"icon": "shopping-cart", "color": "#F59E0B"},
    "avg_order_value": {"icon": "credit-card", "color": "#EF4444"},
    "stock_level": {"icon": "package", "color": "#6366F1"},
    # Distribution
    "receivables": {"icon": "banknote", "color": "#DC2626"},
    "revenue_per_rep": {"icon": "user-check", "color": "#0891B2"},
    "stock_rotation": {"icon": "refresh-cw", "color": "#7C3AED"},
    "return_rate": {"icon": "undo-2", "color": "#EA580C"},
    # Retail
    "revenue_per_store": {"icon": "store", "color": "#0D9488"},
    "conversion_rate": {"icon": "percent", "color": "#CA8A04"},
    # Industrie
    "production_cost": {"icon": "factory", "color": "#B91C1C"},
    "yield_rate": {"icon": "gauge", "color": "#15803D"},
    "defect_rate": {"icon": "alert-triangle", "color": "#DC2626"},
    "on_time_delivery": {"icon": "clock", "color": "#2563EB"},
    # Transport
    "cost_per_km": {"icon": "fuel", "color": "#EA580C"},
    "fill_rate": {"icon": "container", "color": "#0891B2"},
    "fuel_consumption": {"icon": "droplet", "color": "#B45309"},
    "deliveries_count": {"icon": "truck", "color": "#15803D"},
    # Restaurant
    "food_cost_pct": {"icon": "utensils", "color": "#DC2626"},
    "dishes_sold": {"icon": "chef-hat", "color": "#7C3AED"},
    "waste_rate": {"icon": "trash-2", "color": "#EA580C"},
    # E-commerce
    "cac": {"icon": "target", "color": "#B91C1C"},
    "ltv": {"icon": "heart", "color": "#15803D"},
    "return_rate_ecom": {"icon": "package-x", "color": "#EA580C"},
    "revenue_per_channel": {"icon": "globe", "color": "#0891B2"},
    # Clinique
    "revenue_per_doctor": {"icon": "stethoscope", "color": "#2563EB"},
    "patient_count": {"icon": "users", "color": "#7C3AED"},
    "occupancy_rate": {"icon": "bed", "color": "#0D9488"},
    # Pharmacie
    "revenue_per_pharmacy": {"icon": "pill", "color": "#2563EB"},
    "prescriptions_per_day": {"icon": "clipboard-list", "color": "#7C3AED"},
    "critical_stock": {"icon": "alert-circle", "color": "#DC2626"},
    # Immobilier
    "sales_count": {"icon": "key", "color": "#15803D"},
    "commercialization_rate": {"icon": "percent", "color": "#2563EB"},
    "price_per_sqm": {"icon": "ruler", "color": "#7C3AED"},
    "avg_sale_delay": {"icon": "calendar", "color": "#EA580C"},
    # Hotel
    "revpar": {"icon": "hotel", "color": "#2563EB"},
    "adr": {"icon": "banknote", "color": "#15803D"},
    "occupancy_rate_hotel": {"icon": "bed", "color": "#0D9488"},
    "fb_revenue": {"icon": "utensils", "color": "#F59E0B"},
    # Services
    "billable_hours": {"icon": "clock", "color": "#7C3AED"},
    "collection_rate": {"icon": "wallet", "color": "#15803D"},
    "active_contracts": {"icon": "file-text", "color": "#2563EB"},
    "margin_per_project": {"icon": "folder", "color": "#0891B2"},
    # Agriculture
    "yield_per_ha": {"icon": "sprout", "color": "#15803D"},
    "cost_per_ton": {"icon": "scale", "color": "#EA580C"},
    "harvest_stock": {"icon": "warehouse", "color": "#7C3AED"},
}


def _detect_available_fields(db: Client, org_id: str) -> set[str]:
    """Detect which mapped fields exist in the organization's data sources."""
    result = (
        db.table("data_sources")
        .select("column_mappings")
        .eq("organization_id", org_id)
        .eq("status", "ready")
        .execute()
    )

    fields: set[str] = set()
    for source in result.data or []:
        mappings = source.get("column_mappings") or []
        for mapping in mappings:
            mapped = mapping.get("mapped") or mapping.get("kpi_type")
            if mapped:
                fields.add(mapped)

    return fields


def build_dashboard_config(
    db: Client,
    org_id: str,
    sector_slug: str | None = None,
) -> Dict[str, Any]:
    """
    Build a dashboard configuration based on sector + available data.

    1. Get sector's desired KPIs from registry.
    2. Cross-reference with available data columns.
    3. Build KPI cards and chart configs.
    """
    available_fields = _detect_available_fields(db, org_id)

    # Get sector-specific KPI list or default
    if sector_slug:
        desired_kpis = get_sector_primary_kpis(sector_slug)
        sector_config = get_sector(sector_slug)
        sector_charts = sector_config.get("charts", []) if sector_config else []
        sector_rankings = sector_config.get("rankings", []) if sector_config else []
    else:
        desired_kpis = ["revenue", "margin", "client_count", "order_count", "avg_order_value", "stock_level"]
        sector_charts = []
        sector_rankings = []

    kpi_cards: List[Dict[str, Any]] = []
    charts: List[Dict[str, Any]] = []

    for position, kpi_slug in enumerate(desired_kpis):
        display = KPI_DISPLAY.get(kpi_slug, {"icon": "bar-chart", "color": "#64748B"})

        try:
            kpi_enum = KpiType(kpi_slug)
            from app.services.kpi_calculator import KPI_LABELS
            label, unit = KPI_LABELS.get(kpi_enum, (kpi_slug, ""))
        except ValueError:
            label = kpi_slug.replace("_", " ").title()
            unit = ""

        kpi_cards.append({
            "kpi_type": kpi_slug,
            "label": label,
            "unit": unit,
            "icon": display["icon"],
            "color": display["color"],
            "position": position,
            "visible": True,
        })

    # Build chart configs from sector definition
    if sector_charts:
        for i, chart_def in enumerate(sector_charts):
            display = KPI_DISPLAY.get(chart_def["kpi"], {"icon": "bar-chart", "color": "#2563EB"})
            charts.append({
                "kpi_type": chart_def["kpi"],
                "title": chart_def["title"],
                "chart_type": chart_def["type"],
                "color": display["color"],
                "position": i,
                "visible": True,
            })
    else:
        # Default charts for non-sector dashboards
        for i, kpi_slug in enumerate(desired_kpis[:3]):
            display = KPI_DISPLAY.get(kpi_slug, {"icon": "bar-chart", "color": "#2563EB"})
            charts.append({
                "kpi_type": kpi_slug,
                "title": kpi_cards[i]["label"] if i < len(kpi_cards) else kpi_slug,
                "chart_type": "line" if kpi_slug in ("revenue", "margin", "avg_order_value") else "bar",
                "color": display["color"],
                "position": i,
                "visible": True,
            })

    dashboard_config = {
        "organization_id": org_id,
        "sector_slug": sector_slug,
        "kpi_cards": kpi_cards,
        "charts": charts,
        "rankings": sector_rankings,
        "layout": sector_slug or "default",
        "available_kpis": desired_kpis,
    }

    logger.info(
        "Built dashboard config for org %s (sector=%s): %d KPIs, %d charts",
        org_id, sector_slug, len(kpi_cards), len(charts),
    )
    return dashboard_config


def save_dashboard_config(db: Client, org_id: str, config: Dict[str, Any]) -> None:
    """Persist the dashboard configuration to the database."""
    db.table("dashboard_configs").upsert({
        "organization_id": org_id,
        "layout": config,
    }, on_conflict="organization_id").execute()


def create_default_alerts(db: Client, org_id: str, sector_slug: str) -> int:
    """Create pre-configured alerts for a sector. Returns count created."""
    default_alerts = get_sector_default_alerts(sector_slug)
    created = 0

    for alert_def in default_alerts:
        db.table("alerts").insert({
            "organization_id": org_id,
            "name": alert_def["name"],
            "kpi_type": alert_def["kpi_type"],
            "condition": alert_def["condition"],
            "threshold": alert_def["threshold"],
            "channels": ["email"],
            "is_active": True,
        }).execute()
        created += 1

    logger.info("Created %d default alerts for org %s (sector=%s)", created, org_id, sector_slug)
    return created
