"""
PilotBI enumeration types.
"""

from __future__ import annotations

from enum import Enum


class PlanTier(str, Enum):
    FREE = "free"
    STARTER = "starter"
    PRO = "pro"
    EQUIPE = "equipe"


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    TRIALING = "trialing"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    UNPAID = "unpaid"
    INCOMPLETE = "incomplete"


class DataSourceType(str, Enum):
    CSV = "csv"
    EXCEL = "excel"
    GOOGLE_SHEETS = "google_sheets"
    API = "api"


class DataSourceStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    READY = "ready"
    ERROR = "error"


class KpiType(str, Enum):
    # Core (all sectors)
    REVENUE = "revenue"
    MARGIN = "margin"
    CLIENT_COUNT = "client_count"
    ORDER_COUNT = "order_count"
    AVG_ORDER_VALUE = "avg_order_value"
    STOCK_LEVEL = "stock_level"

    # Distribution
    RECEIVABLES = "receivables"
    REVENUE_PER_REP = "revenue_per_rep"
    STOCK_ROTATION = "stock_rotation"
    RETURN_RATE = "return_rate"

    # Retail
    REVENUE_PER_STORE = "revenue_per_store"
    CONVERSION_RATE = "conversion_rate"

    # Industrie
    PRODUCTION_COST = "production_cost"
    YIELD_RATE = "yield_rate"
    DEFECT_RATE = "defect_rate"
    ON_TIME_DELIVERY = "on_time_delivery"

    # Transport
    COST_PER_KM = "cost_per_km"
    FILL_RATE = "fill_rate"
    FUEL_CONSUMPTION = "fuel_consumption"
    DELIVERIES_COUNT = "deliveries_count"

    # Restaurant
    FOOD_COST_PCT = "food_cost_pct"
    DISHES_SOLD = "dishes_sold"
    WASTE_RATE = "waste_rate"

    # E-commerce
    CAC = "cac"
    LTV = "ltv"
    RETURN_RATE_ECOM = "return_rate_ecom"
    REVENUE_PER_CHANNEL = "revenue_per_channel"

    # Clinique
    REVENUE_PER_DOCTOR = "revenue_per_doctor"
    PATIENT_COUNT = "patient_count"
    OCCUPANCY_RATE = "occupancy_rate"

    # Pharmacie
    REVENUE_PER_STORE_PHARMA = "revenue_per_pharmacy"
    PRESCRIPTIONS_PER_DAY = "prescriptions_per_day"
    CRITICAL_STOCK = "critical_stock"

    # Immobilier
    SALES_COUNT = "sales_count"
    COMMERCIALIZATION_RATE = "commercialization_rate"
    PRICE_PER_SQM = "price_per_sqm"
    AVG_SALE_DELAY = "avg_sale_delay"

    # Hotel
    REVPAR = "revpar"
    ADR = "adr"
    OCCUPANCY_RATE_HOTEL = "occupancy_rate_hotel"
    FB_REVENUE = "fb_revenue"

    # Services B2B
    BILLABLE_HOURS = "billable_hours"
    COLLECTION_RATE = "collection_rate"
    ACTIVE_CONTRACTS = "active_contracts"
    MARGIN_PER_PROJECT = "margin_per_project"

    # Agriculture
    YIELD_PER_HA = "yield_per_ha"
    COST_PER_TON = "cost_per_ton"
    HARVEST_STOCK = "harvest_stock"


class AlertCondition(str, Enum):
    ABOVE = "above"
    BELOW = "below"
    CHANGE_PCT = "change_pct"


class PeriodType(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
