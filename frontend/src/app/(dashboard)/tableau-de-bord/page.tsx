"use client";

import { useState } from "react";
import { KpiCard } from "@/components/dashboard/kpi-card";
import { DashboardBarChart } from "@/components/dashboard/bar-chart";
import { DashboardLineChart } from "@/components/dashboard/line-chart";
import { DashboardPieChart } from "@/components/dashboard/pie-chart";
import { PeriodFilter } from "@/components/dashboard/period-filter";
import type { KpiCardData } from "@/types/dashboard";
import type { PeriodId } from "@/lib/constants";
import { CalendarDays } from "lucide-react";

// ---------------------------------------------------------------------------
// Realistic demo data for a Moroccan SME (distribution company)
// ---------------------------------------------------------------------------

const DEMO_KPIS: KpiCardData[] = [
  {
    type: "revenue",
    label: "Chiffre d'affaires",
    value: 2_847_500,
    previousValue: 2_615_000,
    changePercent: 8.9,
    trend: "up",
    format: "currency",
    icon: "revenue",
    sparklineData: [180, 220, 195, 245, 230, 260, 285, 310, 275, 320, 295, 340],
  },
  {
    type: "net_margin",
    label: "Marge nette",
    value: 0.142,
    previousValue: 0.128,
    changePercent: 10.9,
    trend: "up",
    format: "percent",
    icon: "net_margin",
    sparklineData: [12, 11, 13, 12, 14, 13, 15, 14, 13, 14, 15, 14],
  },
  {
    type: "active_clients",
    label: "Clients actifs",
    value: 347,
    previousValue: 312,
    changePercent: 11.2,
    trend: "up",
    format: "number",
    icon: "active_clients",
    sparklineData: [280, 290, 300, 295, 310, 305, 320, 315, 330, 325, 340, 347],
  },
  {
    type: "critical_stock",
    label: "Stock critique",
    value: 12,
    previousValue: 8,
    changePercent: -50.0,
    trend: "down",
    format: "number",
    icon: "critical_stock",
    sparklineData: [5, 6, 4, 7, 8, 6, 9, 7, 10, 8, 11, 12],
  },
];

const DEMO_MONTHLY_SALES = [
  { label: "Jan", value: 1_950_000 },
  { label: "Fev", value: 2_120_000 },
  { label: "Mar", value: 2_340_000 },
  { label: "Avr", value: 2_080_000 },
  { label: "Mai", value: 2_560_000 },
  { label: "Jun", value: 2_410_000 },
  { label: "Jul", value: 2_180_000 },
  { label: "Aou", value: 1_870_000 },
  { label: "Sep", value: 2_650_000 },
  { label: "Oct", value: 2_780_000 },
  { label: "Nov", value: 2_920_000 },
  { label: "Dec", value: 2_847_500 },
];

const DEMO_REVENUE_EVOLUTION = [
  { label: "Jan", value: 1_950_000 },
  { label: "Fev", value: 2_120_000 },
  { label: "Mar", value: 2_340_000 },
  { label: "Avr", value: 2_080_000 },
  { label: "Mai", value: 2_560_000 },
  { label: "Jun", value: 2_410_000 },
  { label: "Jul", value: 2_180_000 },
  { label: "Aou", value: 1_870_000 },
  { label: "Sep", value: 2_650_000 },
  { label: "Oct", value: 2_780_000 },
  { label: "Nov", value: 2_920_000 },
  { label: "Dec", value: 3_100_000 },
];

const DEMO_CATEGORY_DISTRIBUTION = [
  { name: "Alimentaire", value: 1_280_000 },
  { name: "Boissons", value: 620_000 },
  { name: "Hygiene", value: 410_000 },
  { name: "Entretien", value: 320_000 },
  { name: "Electronique", value: 217_500 },
];

export default function TableauDeBordPage() {
  const [period, setPeriod] = useState<PeriodId>("this_month");

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-ink tracking-tight">
            Tableau de bord
          </h1>
          <p className="mt-1 text-sm text-ink-3 flex items-center gap-1.5">
            <CalendarDays className="h-3.5 w-3.5" />
            Derniere mise a jour : 6 avril 2026 a 09:15
          </p>
        </div>
        <PeriodFilter value={period} onChange={setPeriod} />
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4 stagger-children">
        {DEMO_KPIS.map((kpi) => (
          <KpiCard key={kpi.type} data={kpi} />
        ))}
      </div>

      {/* Main bar chart */}
      <DashboardBarChart
        title="Ventes mensuelles"
        data={DEMO_MONTHLY_SALES}
      />

      {/* Two-column charts */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <DashboardLineChart
          title="Evolution du chiffre d'affaires"
          data={DEMO_REVENUE_EVOLUTION}
        />
        <DashboardPieChart
          title="Repartition par categorie"
          data={DEMO_CATEGORY_DISTRIBUTION}
        />
      </div>
    </div>
  );
}
