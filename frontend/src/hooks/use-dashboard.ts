"use client";

import { useCallback, useEffect, useState } from "react";
import { api } from "@/lib/api";
import type {
  DashboardKpiResponse,
  DashboardChartResponse,
} from "@/types/api";
import type { DashboardFilters } from "@/types/dashboard";

interface DashboardState {
  kpis: DashboardKpiResponse | null;
  charts: DashboardChartResponse | null;
  isLoading: boolean;
  error: string | null;
}

export function useDashboard(filters: DashboardFilters) {
  const [state, setState] = useState<DashboardState>({
    kpis: null,
    charts: null,
    isLoading: true,
    error: null,
  });

  const fetchDashboard = useCallback(async () => {
    try {
      setState((prev) => ({ ...prev, isLoading: true, error: null }));

      const params: Record<string, string> = {
        period: filters.period,
      };
      if (filters.customStart) params.start = filters.customStart;
      if (filters.customEnd) params.end = filters.customEnd;

      const [kpis, charts] = await Promise.all([
        api.get<DashboardKpiResponse>("/dashboard/kpis", { params }),
        api.get<DashboardChartResponse>("/dashboard", { params }),
      ]);

      setState({
        kpis,
        charts,
        isLoading: false,
        error: null,
      });
    } catch (err) {
      setState((prev) => ({
        ...prev,
        isLoading: false,
        error:
          err instanceof Error ? err.message : "Erreur lors du chargement",
      }));
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
