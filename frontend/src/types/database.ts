// ---------------------------------------------------------------------------
// Types mirroring the Supabase / Postgres schema
// ---------------------------------------------------------------------------

export interface Organization {
  id: string;
  name: string;
  sector: string | null;
  city: string | null;
  employee_count: number | null;
  created_at: string;
  updated_at: string;
}

export interface Profile {
  id: string; // matches auth.users.id
  organization_id: string;
  full_name: string;
  email: string;
  avatar_url: string | null;
  role: "owner" | "admin" | "member";
  language: "fr" | "ar";
  onboarding_completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface Subscription {
  id: string;
  organization_id: string;
  plan: "starter" | "pro" | "equipe";
  status: "active" | "trialing" | "past_due" | "canceled" | "incomplete";
  stripe_customer_id: string | null;
  stripe_subscription_id: string | null;
  current_period_start: string;
  current_period_end: string;
  created_at: string;
  updated_at: string;
}

export interface DataSource {
  id: string;
  organization_id: string;
  name: string;
  type: "excel" | "csv" | "google_sheets" | "odoo" | "sage";
  status: "pending" | "processing" | "active" | "error";
  file_url: string | null;
  row_count: number;
  column_count: number;
  last_synced_at: string | null;
  error_message: string | null;
  metadata: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
}

export interface DataRow {
  id: string;
  data_source_id: string;
  row_index: number;
  data: Record<string, unknown>;
  created_at: string;
}

export interface KpiSnapshot {
  id: string;
  organization_id: string;
  kpi_type: string;
  value: number;
  previous_value: number | null;
  change_percent: number | null;
  period_start: string;
  period_end: string;
  created_at: string;
}

export interface Report {
  id: string;
  organization_id: string;
  title: string;
  period_label: string;
  status: "draft" | "generating" | "ready" | "error";
  summary: string | null;
  content: ReportContent | null;
  generated_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface ReportContent {
  resume: string;
  analyse: string;
  anomalies: string[];
  actions: string[];
}

export interface Alert {
  id: string;
  organization_id: string;
  name: string;
  kpi_type: string;
  condition: "above" | "below" | "change_above" | "change_below";
  threshold: number;
  is_active: boolean;
  notification_channels: ("email" | "sms" | "in_app")[];
  created_at: string;
  updated_at: string;
}

export interface AlertHistory {
  id: string;
  alert_id: string;
  triggered_value: number;
  message: string;
  is_read: boolean;
  triggered_at: string;
}
