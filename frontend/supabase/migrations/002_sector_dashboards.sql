-- PilotBI Migration 002: Sector-specific dashboards
-- Run in Supabase SQL Editor after 001_initial_schema.sql

-- Add sector slug to organizations
ALTER TABLE organizations ADD COLUMN IF NOT EXISTS sector_slug TEXT;

-- Dashboard insights cache (AI-generated, cached 1h)
CREATE TABLE IF NOT EXISTS dashboard_insights (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  generated_at TIMESTAMPTZ DEFAULT NOW(),
  expires_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_insights_org ON dashboard_insights(organization_id, expires_at DESC);

-- Allow RLS on insights
ALTER TABLE dashboard_insights ENABLE ROW LEVEL SECURITY;

CREATE POLICY "insights_select" ON dashboard_insights
  FOR SELECT USING (organization_id = get_user_org_id());

CREATE POLICY "insights_insert" ON dashboard_insights
  FOR INSERT WITH CHECK (organization_id = get_user_org_id());

-- Remove strict CHECK constraint on kpi_type to allow sector-specific types
ALTER TABLE kpi_snapshots DROP CONSTRAINT IF EXISTS kpi_snapshots_kpi_type_check;

-- Add welcome_seen flag to profiles for first-time modal
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS welcome_seen BOOLEAN DEFAULT FALSE;

-- Add affiliate tracking for fiduciary partners
CREATE TABLE IF NOT EXISTS affiliates (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  code TEXT UNIQUE NOT NULL,
  commission_pct INTEGER DEFAULT 30,
  total_referrals INTEGER DEFAULT 0,
  total_earned NUMERIC DEFAULT 0,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS referrals (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  affiliate_id UUID NOT NULL REFERENCES affiliates(id) ON DELETE CASCADE,
  referred_org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'active', 'paid')),
  commission_amount NUMERIC DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE affiliates ENABLE ROW LEVEL SECURITY;
ALTER TABLE referrals ENABLE ROW LEVEL SECURITY;

CREATE POLICY "affiliates_select" ON affiliates
  FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "referrals_select" ON referrals
  FOR SELECT USING (affiliate_id IN (SELECT id FROM affiliates WHERE user_id = auth.uid()));

-- Free analysis leads (for /analyse-gratuite viral page)
CREATE TABLE IF NOT EXISTS free_analysis_leads (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email TEXT NOT NULL,
  company_name TEXT,
  file_path TEXT,
  insights JSONB,
  converted BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
