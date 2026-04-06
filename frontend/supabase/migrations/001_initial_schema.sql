-- PilotBI Database Schema
-- Run this in Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ══════════════════════════════════════
-- ORGANIZATIONS
-- ══════════════════════════════════════
CREATE TABLE organizations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  sector TEXT,
  employee_count INTEGER,
  city TEXT,
  phone TEXT,
  language TEXT DEFAULT 'fr' CHECK (language IN ('fr', 'ar')),
  onboarding_completed BOOLEAN DEFAULT FALSE,
  stripe_customer_id TEXT UNIQUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ══════════════════════════════════════
-- PROFILES (extends auth.users)
-- ══════════════════════════════════════
CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
  full_name TEXT NOT NULL,
  role TEXT DEFAULT 'owner' CHECK (role IN ('owner', 'admin', 'viewer')),
  avatar_url TEXT,
  is_platform_admin BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_profiles_org ON profiles(organization_id);

-- ══════════════════════════════════════
-- SUBSCRIPTIONS
-- ══════════════════════════════════════
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  organization_id UUID UNIQUE REFERENCES organizations(id) ON DELETE CASCADE,
  stripe_subscription_id TEXT UNIQUE,
  plan TEXT NOT NULL DEFAULT 'starter' CHECK (plan IN ('starter', 'pro', 'equipe')),
  status TEXT NOT NULL DEFAULT 'trialing' CHECK (status IN ('trialing', 'active', 'past_due', 'canceled', 'incomplete')),
  trial_ends_at TIMESTAMPTZ,
  current_period_start TIMESTAMPTZ,
  current_period_end TIMESTAMPTZ,
  cancel_at_period_end BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ══════════════════════════════════════
-- DATA SOURCES
-- ══════════════════════════════════════
CREATE TABLE data_sources (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  type TEXT NOT NULL CHECK (type IN ('excel', 'csv', 'google_sheets', 'odoo', 'sage')),
  name TEXT NOT NULL,
  file_path TEXT,
  connection_config JSONB,
  column_mapping JSONB,
  last_synced_at TIMESTAMPTZ,
  row_count INTEGER DEFAULT 0,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'ready', 'error')),
  error_message TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_data_sources_org ON data_sources(organization_id);

-- ══════════════════════════════════════
-- DATA ROWS (flexible JSONB storage)
-- ══════════════════════════════════════
CREATE TABLE data_rows (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  source_id UUID NOT NULL REFERENCES data_sources(id) ON DELETE CASCADE,
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  date DATE,
  data JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_data_rows_org_date ON data_rows(organization_id, date);
CREATE INDEX idx_data_rows_source ON data_rows(source_id);

-- ══════════════════════════════════════
-- KPI SNAPSHOTS (pre-calculated metrics)
-- ══════════════════════════════════════
CREATE TABLE kpi_snapshots (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  period DATE NOT NULL,
  period_type TEXT NOT NULL CHECK (period_type IN ('daily', 'weekly', 'monthly')),
  kpi_type TEXT NOT NULL CHECK (kpi_type IN ('revenue', 'margin', 'client_count', 'order_count', 'avg_order_value', 'stock_level')),
  value NUMERIC NOT NULL,
  previous_value NUMERIC,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_kpi_unique ON kpi_snapshots(organization_id, period, period_type, kpi_type);
CREATE INDEX idx_kpi_org_period ON kpi_snapshots(organization_id, period_type, period);

-- ══════════════════════════════════════
-- DASHBOARD CONFIGS
-- ══════════════════════════════════════
CREATE TABLE dashboard_configs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  organization_id UUID UNIQUE REFERENCES organizations(id) ON DELETE CASCADE,
  layout JSONB NOT NULL DEFAULT '[]'::jsonb,
  filters JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ══════════════════════════════════════
-- REPORTS (AI-generated)
-- ══════════════════════════════════════
CREATE TABLE reports (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  period DATE NOT NULL,
  title TEXT NOT NULL,
  summary TEXT,
  content JSONB NOT NULL DEFAULT '{}'::jsonb,
  actions JSONB,
  anomalies JSONB,
  status TEXT DEFAULT 'generating' CHECK (status IN ('generating', 'ready', 'error')),
  ai_model TEXT,
  token_usage JSONB,
  sent_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_reports_org ON reports(organization_id, period DESC);

-- ══════════════════════════════════════
-- ALERTS
-- ══════════════════════════════════════
CREATE TABLE alerts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  kpi_type TEXT NOT NULL,
  condition TEXT NOT NULL CHECK (condition IN ('above', 'below', 'change_pct')),
  threshold NUMERIC NOT NULL,
  channels TEXT[] NOT NULL DEFAULT ARRAY['email'],
  is_active BOOLEAN DEFAULT TRUE,
  last_triggered_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_alerts_org ON alerts(organization_id);

-- ══════════════════════════════════════
-- ALERT HISTORY
-- ══════════════════════════════════════
CREATE TABLE alert_history (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  alert_id UUID NOT NULL REFERENCES alerts(id) ON DELETE CASCADE,
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  triggered_value NUMERIC,
  message TEXT,
  channels_sent TEXT[],
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_alert_history_org ON alert_history(organization_id, created_at DESC);

-- ══════════════════════════════════════
-- ROW LEVEL SECURITY
-- ══════════════════════════════════════
ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE data_sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE data_rows ENABLE ROW LEVEL SECURITY;
ALTER TABLE kpi_snapshots ENABLE ROW LEVEL SECURITY;
ALTER TABLE dashboard_configs ENABLE ROW LEVEL SECURITY;
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE alert_history ENABLE ROW LEVEL SECURITY;

-- Helper function to get user's org
CREATE OR REPLACE FUNCTION get_user_org_id()
RETURNS UUID AS $$
  SELECT organization_id FROM profiles WHERE id = auth.uid()
$$ LANGUAGE SQL SECURITY DEFINER STABLE;

-- Organizations: users see their own org
CREATE POLICY "org_select" ON organizations FOR SELECT USING (id = get_user_org_id());
CREATE POLICY "org_update" ON organizations FOR UPDATE USING (id = get_user_org_id());

-- Profiles: users see profiles in their org
CREATE POLICY "profiles_select" ON profiles FOR SELECT USING (organization_id = get_user_org_id());
CREATE POLICY "profiles_update" ON profiles FOR UPDATE USING (id = auth.uid());
CREATE POLICY "profiles_insert" ON profiles FOR INSERT WITH CHECK (id = auth.uid());

-- Subscriptions: org isolation
CREATE POLICY "sub_select" ON subscriptions FOR SELECT USING (organization_id = get_user_org_id());

-- Data sources: org isolation
CREATE POLICY "ds_select" ON data_sources FOR SELECT USING (organization_id = get_user_org_id());
CREATE POLICY "ds_insert" ON data_sources FOR INSERT WITH CHECK (organization_id = get_user_org_id());
CREATE POLICY "ds_update" ON data_sources FOR UPDATE USING (organization_id = get_user_org_id());
CREATE POLICY "ds_delete" ON data_sources FOR DELETE USING (organization_id = get_user_org_id());

-- Data rows: org isolation
CREATE POLICY "dr_select" ON data_rows FOR SELECT USING (organization_id = get_user_org_id());
CREATE POLICY "dr_insert" ON data_rows FOR INSERT WITH CHECK (organization_id = get_user_org_id());

-- KPI snapshots: org isolation
CREATE POLICY "kpi_select" ON kpi_snapshots FOR SELECT USING (organization_id = get_user_org_id());

-- Dashboard configs: org isolation
CREATE POLICY "dc_select" ON dashboard_configs FOR SELECT USING (organization_id = get_user_org_id());
CREATE POLICY "dc_insert" ON dashboard_configs FOR INSERT WITH CHECK (organization_id = get_user_org_id());
CREATE POLICY "dc_update" ON dashboard_configs FOR UPDATE USING (organization_id = get_user_org_id());

-- Reports: org isolation
CREATE POLICY "reports_select" ON reports FOR SELECT USING (organization_id = get_user_org_id());

-- Alerts: org isolation
CREATE POLICY "alerts_select" ON alerts FOR SELECT USING (organization_id = get_user_org_id());
CREATE POLICY "alerts_insert" ON alerts FOR INSERT WITH CHECK (organization_id = get_user_org_id());
CREATE POLICY "alerts_update" ON alerts FOR UPDATE USING (organization_id = get_user_org_id());
CREATE POLICY "alerts_delete" ON alerts FOR DELETE USING (organization_id = get_user_org_id());

-- Alert history: org isolation
CREATE POLICY "ah_select" ON alert_history FOR SELECT USING (organization_id = get_user_org_id());

-- ══════════════════════════════════════
-- STORAGE BUCKET
-- ══════════════════════════════════════
INSERT INTO storage.buckets (id, name, public) VALUES ('uploads', 'uploads', false)
ON CONFLICT (id) DO NOTHING;

-- Storage policy: users can upload to their org folder
CREATE POLICY "upload_insert" ON storage.objects FOR INSERT
  WITH CHECK (bucket_id = 'uploads' AND (storage.foldername(name))[1] = get_user_org_id()::text);

CREATE POLICY "upload_select" ON storage.objects FOR SELECT
  USING (bucket_id = 'uploads' AND (storage.foldername(name))[1] = get_user_org_id()::text);

-- ══════════════════════════════════════
-- AUTO-UPDATE TRIGGER
-- ══════════════════════════════════════
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_organizations_updated_at BEFORE UPDATE ON organizations
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER trg_subscriptions_updated_at BEFORE UPDATE ON subscriptions
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER trg_dashboard_configs_updated_at BEFORE UPDATE ON dashboard_configs
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ══════════════════════════════════════
-- AUTO-CREATE PROFILE + ORG ON SIGNUP
-- ══════════════════════════════════════
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
DECLARE
  org_id UUID;
BEGIN
  -- Create organization
  INSERT INTO organizations (name) VALUES (COALESCE(NEW.raw_user_meta_data->>'company_name', 'Mon entreprise'))
  RETURNING id INTO org_id;

  -- Create profile
  INSERT INTO profiles (id, organization_id, full_name)
  VALUES (NEW.id, org_id, COALESCE(NEW.raw_user_meta_data->>'full_name', NEW.email));

  -- Create trial subscription
  INSERT INTO subscriptions (organization_id, plan, status, trial_ends_at)
  VALUES (org_id, 'starter', 'trialing', NOW() + INTERVAL '14 days');

  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION handle_new_user();
