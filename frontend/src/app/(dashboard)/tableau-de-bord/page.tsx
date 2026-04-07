"use client";

import { useEffect, useState } from "react";
import { KpiCard } from "@/components/dashboard/kpi-card";
import { DashboardBarChart } from "@/components/dashboard/bar-chart";
import { DashboardLineChart } from "@/components/dashboard/line-chart";
import { DashboardPieChart } from "@/components/dashboard/pie-chart";
import { PeriodFilter } from "@/components/dashboard/period-filter";
import { AiInsightCard } from "@/components/dashboard/ai-insight-card";
import { WelcomeModal } from "@/components/dashboard/welcome-modal";
import { GaugeChart } from "@/components/dashboard/gauge-chart";
import { RankingTable } from "@/components/dashboard/ranking-table";
import { ComparisonChart } from "@/components/dashboard/comparison-chart";
import { useDashboard } from "@/hooks/use-dashboard";
import { useUser } from "@/hooks/use-user";
import type { PeriodId } from "@/lib/constants";
import { CalendarDays, Loader2, FileUp } from "lucide-react";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function TableauDeBordPage() {
  const [period, setPeriod] = useState<PeriodId>("this_month");
  const [showWelcome, setShowWelcome] = useState(false);

  const { user, profile, organization } = useUser();
  const dashboard = useDashboard({ period });

  // Extract data from dashboard response
  const kpiList = dashboard.kpis?.kpis || [];
  const chartList = dashboard.charts ? [
    ...(dashboard.charts.monthly_sales?.length ? [{ kpi_type: "revenue", title: "Ventes mensuelles", chart_type: "bar" as const, data_points: dashboard.charts.monthly_sales }] : []),
    ...(dashboard.charts.revenue_evolution?.length ? [{ kpi_type: "revenue_evo", title: "Evolution du CA", chart_type: "line" as const, data_points: dashboard.charts.revenue_evolution }] : []),
  ] : [];
  const isLoading = dashboard.isLoading;

  // Show welcome modal on first visit
  useEffect(() => {
    if (profile && !profile.welcome_seen) {
      setShowWelcome(true);
    }
  }, [profile]);

  function handleDismissWelcome() {
    setShowWelcome(false);
    // Mark as seen (fire-and-forget)
    if (profile?.id) {
      fetch("/api/profile/welcome-seen", { method: "POST" }).catch(() => {});
    }
  }

  const sectorLabel = organization?.sector_slug
    ? getSectorDisplayName(organization.sector_slug)
    : undefined;

  const hasData = kpiList.length > 0;

  // Separate gauge-type KPIs from regular cards
  const gaugeKpis = kpiList.filter(
    (k) =>
      k.unit === "%" &&
      [
        "food_cost_pct",
        "fill_rate",
        "occupancy_rate",
        "occupancy_rate_hotel",
        "defect_rate",
        "conversion_rate",
        "collection_rate",
        "commercialization_rate",
        "yield_rate",
        "on_time_delivery",
        "waste_rate",
        "return_rate",
        "return_rate_ecom",
      ].includes(k.kpi_type)
  );

  const cardKpis = kpiList.filter((k: any) => !gaugeKpis.includes(k));

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Welcome modal */}
      {showWelcome && (
        <WelcomeModal
          sectorLabel={sectorLabel}
          onDismiss={handleDismissWelcome}
        />
      )}

      {/* Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-ink tracking-tight">
            Tableau de bord
          </h1>
          <p className="mt-1 text-sm text-ink-3 flex items-center gap-1.5">
            <CalendarDays className="h-3.5 w-3.5" />
            {sectorLabel || "Votre activite"} — Mis a jour en temps reel
          </p>
        </div>
        <PeriodFilter value={period} onChange={setPeriod} />
      </div>

      {/* AI Insight Card (Pro+) */}
      <AiInsightCard />

      {isLoading ? (
        <div className="flex items-center justify-center py-20">
          <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
          <span className="ml-3 text-sm text-ink-3">
            Chargement de vos donnees...
          </span>
        </div>
      ) : !hasData ? (
        /* Empty state */
        <div className="flex flex-col items-center justify-center py-20 text-center">
          <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-50">
            <FileUp className="h-8 w-8 text-blue-600" />
          </div>
          <h2 className="text-lg font-bold text-ink">
            Uploadez vos donnees pour commencer
          </h2>
          <p className="mt-2 max-w-sm text-sm text-ink-3">
            Importez votre fichier Excel ou CSV et votre dashboard
            personnalise sera pret en 30 secondes.
          </p>
          <Link href="/donnees/upload">
            <Button className="mt-6 bg-blue-600 hover:bg-blue-700 text-white">
              <FileUp className="mr-2 h-4 w-4" />
              Importer mes donnees
            </Button>
          </Link>
        </div>
      ) : (
        <>
          {/* KPI Cards */}
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 stagger-children">
            {cardKpis.map((kpi) => (
              <KpiCard
                key={kpi.kpi_type}
                data={{
                  type: kpi.kpi_type,
                  label: kpi.label,
                  value: kpi.value,
                  previousValue: kpi.previous_value ?? null,
                  changePercent: kpi.change_pct ?? null,
                  trend:
                    kpi.change_pct === null || kpi.change_pct === undefined
                      ? "stable"
                      : kpi.change_pct > 0
                        ? "up"
                        : kpi.change_pct < 0
                          ? "down"
                          : "stable",
                  format: kpi.unit === "MAD" ? "currency" : kpi.unit === "%" ? "percent" : "number",
                  icon: kpi.kpi_type,
                }}
              />
            ))}
          </div>

          {/* Gauges row (for percentage KPIs) */}
          {gaugeKpis.length > 0 && (
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {gaugeKpis.map((kpi) => (
                <GaugeChart
                  key={kpi.kpi_type}
                  title={kpi.label}
                  value={kpi.value}
                  unit="%"
                />
              ))}
            </div>
          )}

          {/* Charts */}
          {chartList.length > 0 && (
            <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
              {chartList.map((chart: any) =>
                chart.chart_type === "bar" ? (
                  <DashboardBarChart
                    key={chart.kpi_type}
                    title={chart.title}
                    data={chart.data_points}
                  />
                ) : chart.chart_type === "pie" ? (
                  <DashboardPieChart
                    key={chart.kpi_type}
                    title={chart.title}
                    data={chart.data_points.map((p: any) => ({
                      name: p.label,
                      value: p.value,
                    }))}
                  />
                ) : (
                  <DashboardLineChart
                    key={chart.kpi_type}
                    title={chart.title}
                    data={chart.data_points}
                  />
                )
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
}

function getSectorDisplayName(slug: string): string {
  const map: Record<string, string> = {
    distribution: "Distribution & Commerce de Gros",
    retail: "Retail & Chaines de Magasins",
    industrie: "Industrie & Fabrication",
    transport: "Transport & Logistique",
    restaurant: "Restaurants & F&B",
    ecommerce: "E-commerce",
    clinique: "Cliniques & Sante",
    pharmacie: "Pharmacies",
    immobilier: "Immobilier & Promotion",
    hotel: "Hotels & Riads",
    services: "Services B2B",
    agriculture: "Agriculture",
  };
  return map[slug] || slug;
}
