// ---------------------------------------------------------------------------
// Dashboard-specific frontend types
// ---------------------------------------------------------------------------

import type { KpiType } from "@/lib/constants";

export interface KpiCardData {
  type: string;
  label: string;
  value: number;
  previousValue: number | null;
  changePercent: number | null;
  trend: "up" | "down" | "stable";
  format: "currency" | "percent" | "number";
  icon: string;
  sparklineData?: number[];
}

export interface ChartConfig {
  id: string;
  title: string;
  type: "bar" | "line" | "pie" | "area";
  dataKey: string;
  color: string;
  data: ChartPoint[];
}

export interface ChartPoint {
  label: string;
  value: number;
  [key: string]: string | number;
}

export interface DashboardLayout {
  kpis: KpiCardData[];
  charts: ChartConfig[];
  period: {
    id: string;
    label: string;
    start: string;
    end: string;
  };
  hasData: boolean;
  lastUpdated: string | null;
}

export interface DashboardFilters {
  period: string;
  customStart?: string;
  customEnd?: string;
}
