"""
Dashboard configuration builder.

Builds a default dashboard layout based on which KPIs are available
for a given organization.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from supabase import Client

from app.models.enums import KpiType

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Default dashboard layout configuration
# ---------------------------------------------------------------------------

# Each KPI defines its default card and chart settings
DEFAULT_KPI_CONFIG: Dict[str, Dict[str, Any]] = {
    KpiType.REVENUE.value: {
        "label": "Chiffre d'Affaires",
        "unit": "MAD",
        "icon": "trending-up",
        "color": "#2563EB",
        "chart_type": "line",
        "position": 0,
    },
    KpiType.MARGIN.value: {
        "label": "Marge",
        "unit": "MAD",
        "icon": "bar-chart-2",
        "color": "#10B981",
        "chart_type": "line",
        "position": 1,
    },
    KpiType.CLIENT_COUNT.value: {
        "label": "Nombre de Clients",
        "unit": "",
        "icon": "users",
        "color": "#8B5CF6",
        "chart_type": "bar",
        "position": 2,
    },
    KpiType.ORDER_COUNT.value: {
        "label": "Nombre de Commandes",
        "unit": "",
        "icon": "shopping-cart",
        "color": "#F59E0B",
        "chart_type": "bar",
        "position": 3,
    },
    KpiType.AVG_ORDER_VALUE.value: {
        "label": "Panier Moyen",
        "unit": "MAD",
        "icon": "credit-card",
        "color": "#EF4444",
        "chart_type": "line",
        "position": 4,
    },
    KpiType.STOCK_LEVEL.value: {
        "label": "Niveau de Stock",
        "unit": "",
        "icon": "package",
        "color": "#6366F1",
        "chart_type": "bar",
        "position": 5,
    },
}


def _detect_available_kpis(db: Client, org_id: str) -> List[str]:
    """
    Detect which KPI types have data for the organization by examining
    the column mappings of ready data sources.
    """
    result = (
        db.table("data_sources")
        .select("column_mappings")
        .eq("organization_id", org_id)
        .eq("status", "ready")
        .execute()
    )

    available_fields: set[str] = set()
    for source in result.data or []:
        mappings = source.get("column_mappings") or []
        for mapping in mappings:
            kpi = mapping.get("kpi_type")
            if kpi:
                available_fields.add(kpi)

    # Map fields to KPI types
    field_to_kpi = {
        "revenue": KpiType.REVENUE.value,
        "cost": KpiType.MARGIN.value,
        "margin": KpiType.MARGIN.value,
        "client_name": KpiType.CLIENT_COUNT.value,
        "invoice_id": KpiType.ORDER_COUNT.value,
        "unit_price": KpiType.AVG_ORDER_VALUE.value,
        "stock_level": KpiType.STOCK_LEVEL.value,
    }

    kpi_types: set[str] = set()
    for field in available_fields:
        kpi = field_to_kpi.get(field)
        if kpi:
            kpi_types.add(kpi)

    # Revenue is needed for avg_order_value
    if KpiType.AVG_ORDER_VALUE.value in kpi_types and KpiType.REVENUE.value not in kpi_types:
        kpi_types.discard(KpiType.AVG_ORDER_VALUE.value)

    return sorted(kpi_types)


def build_dashboard_config(db: Client, org_id: str) -> Dict[str, Any]:
    """
    Build a default dashboard configuration based on available KPIs.

    Returns a JSON-serializable dict with dashboard layout info.
    """
    available = _detect_available_kpis(db, org_id)

    kpi_cards: List[Dict[str, Any]] = []
    charts: List[Dict[str, Any]] = []

    for kpi_type in available:
        config = DEFAULT_KPI_CONFIG.get(kpi_type)
        if not config:
            continue

        kpi_cards.append({
            "kpi_type": kpi_type,
            "label": config["label"],
            "unit": config["unit"],
            "icon": config["icon"],
            "color": config["color"],
            "position": config["position"],
            "visible": True,
        })

        charts.append({
            "kpi_type": kpi_type,
            "title": config["label"],
            "chart_type": config["chart_type"],
            "color": config["color"],
            "position": config["position"],
            "visible": True,
        })

    # Sort by position
    kpi_cards.sort(key=lambda x: x["position"])
    charts.sort(key=lambda x: x["position"])

    dashboard_config = {
        "organization_id": org_id,
        "kpi_cards": kpi_cards,
        "charts": charts,
        "layout": "default",
        "available_kpis": available,
    }

    logger.info("Built dashboard config for org %s: %d KPIs available", org_id, len(available))
    return dashboard_config


def save_dashboard_config(db: Client, org_id: str, config: Dict[str, Any]) -> None:
    """Persist the dashboard configuration to the database."""
    db.table("dashboard_configs").upsert({
        "organization_id": org_id,
        "config": config,
    }, on_conflict="organization_id").execute()
