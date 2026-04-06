"""
PilotBI Pydantic schemas for request / response serialization.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from app.models.enums import (
    AlertCondition,
    DataSourceStatus,
    DataSourceType,
    KpiType,
    PeriodType,
    PlanTier,
    SubscriptionStatus,
)


# ---------- Upload / Data Sources ----------

class UploadResponse(BaseModel):
    id: str
    filename: str
    file_type: DataSourceType
    status: DataSourceStatus
    created_at: datetime


class ColumnMapping(BaseModel):
    original_name: str
    mapped_name: Optional[str] = None
    kpi_type: Optional[KpiType] = None
    detected: bool = False


class ColumnMappingUpdate(BaseModel):
    mappings: List[ColumnMapping]


class DataSourceResponse(BaseModel):
    id: str
    organization_id: str
    filename: str
    file_type: DataSourceType
    status: DataSourceStatus
    row_count: Optional[int] = None
    column_mappings: Optional[List[ColumnMapping]] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class DataSourceList(BaseModel):
    items: List[DataSourceResponse]
    total: int


# ---------- Dashboard ----------

class KpiData(BaseModel):
    kpi_type: KpiType
    label: str
    value: float
    previous_value: Optional[float] = None
    change_pct: Optional[float] = None
    unit: str = ""
    period: PeriodType = PeriodType.MONTHLY


class ChartDataPoint(BaseModel):
    label: str
    value: float
    category: Optional[str] = None


class ChartData(BaseModel):
    kpi_type: KpiType
    title: str
    chart_type: str = "line"
    data_points: List[ChartDataPoint]
    period: PeriodType = PeriodType.MONTHLY


class DashboardResponse(BaseModel):
    kpis: List[KpiData]
    charts: List[ChartData]
    period: PeriodType
    generated_at: datetime


# ---------- Reports ----------

class ReportSection(BaseModel):
    title: str
    content: str
    order: int


class ReportResponse(BaseModel):
    id: str
    organization_id: str
    title: str
    period: str
    sections: List[ReportSection]
    generated_at: datetime
    created_at: datetime


class ReportList(BaseModel):
    items: List[ReportResponse]
    total: int


class ReportGenerateRequest(BaseModel):
    period: str = Field(..., description="Period string, e.g. '2025-03' for March 2025")
    language: str = Field(default="fr", description="Report language (fr or en)")


# ---------- Alerts ----------

class AlertCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    kpi_type: KpiType
    condition: AlertCondition
    threshold: float
    notify_email: bool = True
    notify_whatsapp: bool = False
    is_active: bool = True


class AlertUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    kpi_type: Optional[KpiType] = None
    condition: Optional[AlertCondition] = None
    threshold: Optional[float] = None
    notify_email: Optional[bool] = None
    notify_whatsapp: Optional[bool] = None
    is_active: Optional[bool] = None


class AlertResponse(BaseModel):
    id: str
    organization_id: str
    name: str
    kpi_type: KpiType
    condition: AlertCondition
    threshold: float
    notify_email: bool
    notify_whatsapp: bool
    is_active: bool
    last_triggered_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class AlertHistoryResponse(BaseModel):
    id: str
    alert_id: str
    alert_name: str
    kpi_type: KpiType
    condition: AlertCondition
    threshold: float
    actual_value: float
    triggered_at: datetime
    notified: bool


# ---------- Billing ----------

class CheckoutRequest(BaseModel):
    plan: PlanTier
    interval: str = Field(..., pattern="^(monthly|annual)$")
    success_url: str
    cancel_url: str


class CheckoutResponse(BaseModel):
    checkout_url: str
    session_id: str


class PortalResponse(BaseModel):
    portal_url: str


class SubscriptionResponse(BaseModel):
    plan: PlanTier
    status: SubscriptionStatus
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    cancel_at_period_end: bool = False
    stripe_customer_id: Optional[str] = None


# ---------- Admin ----------

class AdminUserResponse(BaseModel):
    id: str
    email: str
    full_name: Optional[str] = None
    organization_id: Optional[str] = None
    organization_name: Optional[str] = None
    plan: PlanTier
    created_at: datetime
    last_sign_in: Optional[datetime] = None


class AdminMetricsResponse(BaseModel):
    total_users: int
    total_organizations: int
    active_subscriptions: int
    mrr: float
    users_by_plan: Dict[str, int]
    signups_last_30d: int
    data_sources_count: int
    reports_generated: int


# ---------- Onboarding ----------

class OrganizationCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    industry: Optional[str] = None
    size: Optional[str] = Field(None, description="e.g. '1-10', '11-50', '51-200'")
    city: Optional[str] = None
    phone: Optional[str] = None
