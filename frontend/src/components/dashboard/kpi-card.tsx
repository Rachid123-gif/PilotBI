"use client";

import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";
import type { KpiCardData } from "@/types/dashboard";
import { formatCurrency, formatPercent, formatNumber } from "@/lib/utils";
import {
  DollarSign, Percent, Users, AlertTriangle, ShoppingCart,
  BarChart3, Target, TrendingUp as GrowthIcon, Banknote,
  Truck, Factory, UtensilsCrossed, HeartPulse, Pill,
  Building2, Hotel, Briefcase, Sprout, Clock, Package,
  Fuel, Wallet, FileText, Bed, Scale, Warehouse,
} from "lucide-react";

const ICON_MAP: Record<string, React.ComponentType<{ className?: string }>> = {
  revenue: DollarSign,
  margin: Banknote,
  client_count: Users,
  order_count: ShoppingCart,
  avg_order_value: BarChart3,
  stock_level: Package,
  receivables: Banknote,
  revenue_per_rep: Users,
  stock_rotation: Package,
  return_rate: Package,
  revenue_per_store: Building2,
  conversion_rate: Target,
  production_cost: Factory,
  yield_rate: Target,
  defect_rate: AlertTriangle,
  on_time_delivery: Clock,
  cost_per_km: Fuel,
  fill_rate: Truck,
  fuel_consumption: Fuel,
  deliveries_count: Truck,
  food_cost_pct: UtensilsCrossed,
  dishes_sold: UtensilsCrossed,
  waste_rate: AlertTriangle,
  cac: Target,
  ltv: Users,
  return_rate_ecom: Package,
  revenue_per_channel: ShoppingCart,
  revenue_per_doctor: HeartPulse,
  patient_count: Users,
  occupancy_rate: Bed,
  revenue_per_pharmacy: Pill,
  prescriptions_per_day: FileText,
  critical_stock: AlertTriangle,
  sales_count: Building2,
  commercialization_rate: Target,
  price_per_sqm: Building2,
  avg_sale_delay: Clock,
  revpar: Hotel,
  adr: Banknote,
  occupancy_rate_hotel: Bed,
  fb_revenue: UtensilsCrossed,
  billable_hours: Clock,
  collection_rate: Wallet,
  active_contracts: FileText,
  margin_per_project: Briefcase,
  yield_per_ha: Sprout,
  cost_per_ton: Scale,
  harvest_stock: Warehouse,
  // Legacy
  net_margin: Percent,
  active_clients: Users,
  critical_stock_legacy: AlertTriangle,
  expenses: DollarSign,
  profit: DollarSign,
  orders: ShoppingCart,
  growth_rate: GrowthIcon,
};

const COLOR_MAP: Record<string, string> = {
  revenue: "#2563EB",
  margin: "#10B981",
  client_count: "#8B5CF6",
  order_count: "#F59E0B",
  avg_order_value: "#EF4444",
  stock_level: "#6366F1",
  receivables: "#DC2626",
  food_cost_pct: "#DC2626",
  defect_rate: "#DC2626",
  critical_stock: "#DC2626",
  waste_rate: "#EA580C",
  cost_per_km: "#EA580C",
  revenue_per_store: "#0D9488",
  revenue_per_doctor: "#2563EB",
  revpar: "#2563EB",
  collection_rate: "#15803D",
  occupancy_rate: "#0891B2",
  occupancy_rate_hotel: "#0891B2",
  yield_per_ha: "#15803D",
};

interface KpiCardProps {
  data: KpiCardData;
  className?: string;
}

export function KpiCard({ data, className }: KpiCardProps) {
  const Icon = ICON_MAP[data.type] || BarChart3;
  const accentColor = COLOR_MAP[data.type] || "#2563EB";

  function formatValue(value: number, format: string): string {
    switch (format) {
      case "currency":
        if (value >= 1_000_000) return `${(value / 1_000_000).toFixed(1)}M MAD`;
        if (value >= 1_000) return `${(value / 1_000).toFixed(1)}K MAD`;
        return formatCurrency(value);
      case "percent":
        return `${value.toFixed(1)}%`;
      default:
        return formatNumber(value);
    }
  }

  const isPositive = data.changePercent !== null && data.changePercent > 0;
  const isNegative = data.changePercent !== null && data.changePercent < 0;
  const isNeutral = !isPositive && !isNegative;

  const TrendIcon = isPositive ? TrendingUp : isNegative ? TrendingDown : Minus;

  return (
    <Card
      className={cn(
        "relative overflow-hidden bg-white p-5 shadow-sm transition-all duration-300",
        "hover:shadow-lg hover:-translate-y-0.5 group border-0",
        className
      )}
      style={{ borderTop: `3px solid ${accentColor}` }}
    >
      {/* Background decoration */}
      <div
        className="absolute -right-6 -top-6 h-24 w-24 rounded-full opacity-[0.04] transition-opacity group-hover:opacity-[0.08]"
        style={{ backgroundColor: accentColor }}
      />

      <div className="flex items-start justify-between relative">
        <div
          className="flex h-11 w-11 items-center justify-center rounded-xl transition-transform group-hover:scale-110"
          style={{ backgroundColor: `${accentColor}12` }}
        >
          <Icon className="h-5 w-5 text-blue-600" />
        </div>

        {data.changePercent !== null && (
          <div
            className={cn(
              "flex items-center gap-1 rounded-full px-2.5 py-1 text-xs font-bold tabular-nums",
              isPositive && "bg-emerald-50 text-emerald-700",
              isNegative && "bg-red-50 text-red-600",
              isNeutral && "bg-gray-50 text-gray-500"
            )}
          >
            <TrendIcon className="h-3 w-3" />
            <span>
              {isPositive ? "+" : ""}
              {data.changePercent.toFixed(1)}%
            </span>
          </div>
        )}
      </div>

      <div className="mt-4 relative">
        <p className="text-[13px] font-medium text-gray-500 leading-tight">
          {data.label}
        </p>
        <p className="mt-1.5 text-[28px] font-extrabold text-gray-900 tracking-tight leading-none">
          {formatValue(data.value, data.format)}
        </p>
      </div>

      {/* Sparkline */}
      {data.sparklineData && data.sparklineData.length > 1 && (
        <div className="mt-4 flex items-end gap-[3px] h-10">
          {data.sparklineData.map((val, i) => {
            const max = Math.max(...data.sparklineData!);
            const height = max > 0 ? (val / max) * 100 : 0;
            const isLast = i === data.sparklineData!.length - 1;
            return (
              <div
                key={i}
                className="flex-1 rounded-sm transition-all duration-500"
                style={{
                  height: `${Math.max(height, 6)}%`,
                  backgroundColor: isLast ? accentColor : `${accentColor}30`,
                  transitionDelay: `${i * 30}ms`,
                }}
              />
            );
          })}
        </div>
      )}
    </Card>
  );
}
