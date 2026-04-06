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
    REVENUE = "revenue"
    MARGIN = "margin"
    CLIENT_COUNT = "client_count"
    ORDER_COUNT = "order_count"
    AVG_ORDER_VALUE = "avg_order_value"
    STOCK_LEVEL = "stock_level"


class AlertCondition(str, Enum):
    ABOVE = "above"
    BELOW = "below"
    CHANGE_PCT = "change_pct"


class PeriodType(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
