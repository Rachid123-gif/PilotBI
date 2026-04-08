"use client";

import { useCallback, useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { PeriodId } from "@/lib/constants";

// ---------------------------------------------------------------------------
// Types that match the FastAPI DashboardResponse schema exactly.
// Backend: backend/app/models/schemas.py :: DashboardResponse
// ---------------------------------------------------------------------------

export interface KpiData {
  kpi_type: string;
  label: string;
  value: number;
  previous_value: number | null;
  change_pct: number | null;
  unit: string;
  period: string;
}

export interface ChartDataPoint {
  label: string;
  value: number;
  category?: string | null;
}

export interface ChartData {
  kpi_type: string;
  title: string;
  chart_type: "bar" | "line" | "pie" | string;
  data_points: ChartDataPoint[];
  period: string;
}

export interface DashboardResponse {
  kpis: KpiData[];
  charts: ChartData[];
  period: string;
  generated_at: string;
}

interface DashboardFilters {
  period: PeriodId;
  customStart?: string;
  customEnd?: string;
}

interface DashboardState {
  kpis: KpiData[];
  charts: ChartData[];
  isLoading: boolean;
  error: string | null;
}

/**
 * Map the UI period id to the backend `period` enum + optional date range.
 * Backend accepts period=daily|weekly|monthly and optional start_date/end_date.
 */
function mapPeriod(
  periodId: PeriodId,
  customStart?: string,
  customEnd?: string
): { period: string; start_date?: string; end_date?: string } {
  const isoDate = (d: Date) => d.toISOString().slice(0, 10);
  const now = new Date();

  switch (periodId) {
    case "this_month":
      return { period: "monthly" };

    case "last_month": {
      const start = new Date(now.getFullYear(), now.getMonth() - 1, 1);
      const end = new Date(now.getFullYear(), now.getMonth(), 0);
      return { period: "monthly", start_date: isoDate(start), end_date: isoDate(end) };
    }

    case "last_3_months": {
      const start = new Date(now.getFullYear(), now.getMonth() - 2, 1);
      return { period: "monthly", start_date: isoDate(start), end_date: isoDate(now) };
    }

    case "this_year": {
      const start = new Date(now.getFullYear(), 0, 1);
      return { period: "monthly", start_date: isoDate(start), end_date: isoDate(now) };
    }

    case "custom":
      return {
        period: "monthly",
        start_date: customStart,
        end_date: customEnd,
      };

    default:
      return { period: "monthly" };
  }
}

export function useDashboard(filters: DashboardFilters) {
  const [state, setState] = useState<DashboardState>({
    kpis: [],
    charts: [],
    isLoading: true,
    error: null,
  });

  const fetchDashboard = useCallback(async () => {
    try {
      setState((prev) => ({ ...prev, isLoading: true, error: null }));

      const mapped = mapPeriod(filters.period, filters.customStart, filters.customEnd);
      const params: Record<string, string> = { period: mapped.period };
      if (mapped.start_date) params.start_date = mapped.start_date;
      if (mapped.end_date) params.end_date = mapped.end_date;

      // Single call — /dashboard returns both KPIs and charts.
      // (NEXT_PUBLIC_API_URL already includes the /v1 prefix.)
      const data = await api.get<DashboardResponse>("/dashboard", { params });

      setState({
        kpis: data.kpis ?? [],
        charts: data.charts ?? [],
        isLoading: false,
        error: null,
      });
    } catch (err) {
      setState({
        kpis: [],
        charts: [],
        isLoading: false,
        error: err instanceof Error ? err.message : "Erreur lors du chargement",
      });
    }
  }, [filters.period, filters.customStart, filters.customEnd]);

  useEffect(() => {
    fetchDashboard();
  }, [fetchDashboard]);

  return {
    ...state,
    refresh: fetchDashboard,
  };
}
