// ---------------------------------------------------------------------------
// API response types matching FastAPI backend schemas
// ---------------------------------------------------------------------------

/** Standard paginated response wrapper */
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  has_more: boolean;
}

/** Standard API error response */
export interface ApiErrorResponse {
  detail: string;
  code?: string;
  field_errors?: Record<string, string[]>;
}

/** Dashboard KPI response */
export interface DashboardKpiResponse {
  kpis: KpiItem[];
  period: {
    start: string;
    end: string;
    label: string;
  };
}

export interface KpiItem {
  type: string;
  value: number;
  previous_value: number | null;
  change_percent: number | null;
  trend: "up" | "down" | "stable";
  format: "currency" | "percent" | "number";
}

/** Dashboard chart data response */
export interface DashboardChartResponse {
  monthly_sales: ChartDataPoint[];
  revenue_evolution: ChartDataPoint[];
  category_distribution: PieDataPoint[];
}

export interface ChartDataPoint {
  label: string;
  value: number;
  previous_value?: number;
}

export interface PieDataPoint {
  name: string;
  value: number;
  color?: string;
}

/** Upload response */
export interface UploadResponse {
  data_source_id: string;
  file_name: string;
  row_count: number;
  column_count: number;
  columns: ColumnInfo[];
  preview_rows: Record<string, unknown>[];
}

export interface ColumnInfo {
  name: string;
  type: "string" | "number" | "date" | "boolean";
  sample_values: string[];
  null_count: number;
}

/** Report generation response */
export interface GenerateReportResponse {
  report_id: string;
  status: "generating" | "ready" | "error";
  estimated_seconds?: number;
}

/** Alert create/update request */
export interface AlertRequest {
  name: string;
  kpi_type: string;
  condition: "above" | "below" | "change_above" | "change_below";
  threshold: number;
  is_active: boolean;
  notification_channels: ("email" | "sms" | "in_app")[];
}

/** Onboarding data request */
export interface OnboardingRequest {
  company_name: string;
  city: string;
  employee_count: number;
  sector: string;
}

/** Profile update request */
export interface ProfileUpdateRequest {
  full_name?: string;
  language?: "fr" | "ar";
  avatar_url?: string;
}

/** Billing portal response */
export interface BillingPortalResponse {
  url: string;
}
