"use client";

import { useEffect, useState } from "react";
import { createClient } from "@/lib/supabase/client";
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
import { DashboardSkeleton } from "@/components/dashboard/skeleton";
import { useDashboard } from "@/hooks/use-dashboard";
import { useUser } from "@/hooks/use-user";
import type { PeriodId } from "@/lib/constants";
import { CalendarDays, FileUp, BarChart3, Sparkles, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function TableauDeBordPage() {
  const [period, setPeriod] = useState<PeriodId>("this_month");
  const [showWelcome, setShowWelcome] = useState(false);
  const [hasDismissedWelcome, setHasDismissedWelcome] = useState(false);

  const { user, profile, organization } = useUser();
  const dashboard = useDashboard({ period });

  // Extract data from dashboard response (flat arrays from the backend).
  const kpiList = dashboard.kpis;
  const chartList = dashboard.charts;
  const isLoading = dashboard.isLoading;

  // Show welcome modal on first visit — but never re-show after the user
  // has dismissed it in this session, even if useUser refetches a stale
  // profile where welcome_seen is still false.
  useEffect(() => {
    if (profile && !profile.welcome_seen && !hasDismissedWelcome) {
      setShowWelcome(true);
    }
  }, [profile, hasDismissedWelcome]);

  function handleDismissWelcome() {
    setShowWelcome(false);
    setHasDismissedWelcome(true);
    // Persist welcome_seen=true directly via Supabase (no backend route needed).
    if (profile?.id) {
      const supabase = createClient();
      supabase
        .from("profiles")
        .update({ welcome_seen: true })
        .eq("id", profile.id)
        .then(() => {});
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
        <DashboardSkeleton />
      ) : !hasData ? (
        /* Premium empty state */
        <div className="flex flex-col items-center justify-center py-16 text-center">
          <div className="relative mb-6">
            <div className="flex h-20 w-20 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-50 to-indigo-50 shadow-sm">
              <BarChart3 className="h-10 w-10 text-blue-500" />
            </div>
            <div className="absolute -right-1 -top-1 flex h-7 w-7 items-center justify-center rounded-full bg-amber-400 shadow-md">
              <Sparkles className="h-3.5 w-3.5 text-white" />
            </div>
          </div>
          <h2 className="text-xl font-bold text-gray-900">
            Votre dashboard est pret
          </h2>
          <p className="mt-2 max-w-md text-sm text-gray-500 leading-relaxed">
            Importez votre fichier Excel ou CSV de ventes.
            En 30 secondes, vos KPIs, charts et analyse IA
            seront disponibles.
          </p>
          <div className="mt-8 flex flex-col sm:flex-row gap-3">
            <Link href="/donnees/upload">
              <Button className="bg-blue-600 hover:bg-blue-700 text-white h-11 px-6 font-semibold shadow-md hover:shadow-lg transition-all hover:-translate-y-0.5">
                <FileUp className="mr-2 h-4 w-4" />
                Importer mes donnees
              </Button>
            </Link>
          </div>
          <div className="mt-8 flex items-center gap-6 text-[12px] text-gray-400">
            <span className="flex items-center gap-1.5">
              <span className="inline-block h-1.5 w-1.5 rounded-full bg-emerald-400" />
              Excel, CSV supportes
            </span>
            <span className="flex items-center gap-1.5">
              <span className="inline-block h-1.5 w-1.5 rounded-full bg-emerald-400" />
              Max 5 Mo
            </span>
            <span className="flex items-center gap-1.5">
              <span className="inline-block h-1.5 w-1.5 rounded-full bg-emerald-400" />
              Donnees securisees
            </span>
          </div>
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
