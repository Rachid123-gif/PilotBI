"use client";

import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";
import type { KpiCardData } from "@/types/dashboard";
import { formatCurrency, formatPercent, formatNumber } from "@/lib/utils";
import {
  DollarSign,
  Percent,
  Users,
  AlertTriangle,
  ShoppingCart,
  BarChart3,
  Target,
  TrendingUp as GrowthIcon,
} from "lucide-react";

const ICON_MAP: Record<string, React.ComponentType<{ className?: string }>> = {
  revenue: DollarSign,
  net_margin: Percent,
  active_clients: Users,
  critical_stock: AlertTriangle,
  expenses: DollarSign,
  profit: DollarSign,
  orders: ShoppingCart,
  avg_order_value: BarChart3,
  conversion_rate: Target,
  growth_rate: GrowthIcon,
};

interface KpiCardProps {
  data: KpiCardData;
  className?: string;
}

export function KpiCard({ data, className }: KpiCardProps) {
  const Icon = ICON_MAP[data.type] || BarChart3;

  function formatValue(value: number, format: string): string {
    switch (format) {
      case "currency":
        return formatCurrency(value);
      case "percent":
        return formatPercent(value);
      default:
        return formatNumber(value);
    }
  }

  const trendColor =
    data.trend === "up"
      ? "text-emerald-600 bg-emerald-50"
      : data.trend === "down"
        ? "text-red-600 bg-red-50"
        : "text-ink-3 bg-gray-50";

  const TrendIcon =
    data.trend === "up"
      ? TrendingUp
      : data.trend === "down"
        ? TrendingDown
        : Minus;

  return (
    <Card
      className={cn(
        "relative overflow-hidden border-border/50 bg-white p-5 shadow-sm hover:shadow-md transition-all duration-300 group",
        className
      )}
    >
      {/* Subtle gradient accent */}
      <div className="absolute inset-x-0 top-0 h-0.5 bg-gradient-to-r from-blue-500 to-blue-600 opacity-0 group-hover:opacity-100 transition-opacity" />

      <div className="flex items-start justify-between">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-blue-600">
          <Icon className="h-5 w-5" />
        </div>
        {data.changePercent !== null && (
          <div
            className={cn(
              "flex items-center gap-1 rounded-lg px-2 py-1 text-xs font-semibold",
              trendColor
            )}
          >
            <TrendIcon className="h-3 w-3" />
            <span>
              {data.changePercent > 0 ? "+" : ""}
              {data.changePercent.toFixed(1)}%
            </span>
          </div>
        )}
      </div>

      <div className="mt-4">
        <p className="text-sm font-medium text-ink-3">{data.label}</p>
        <p className="mt-1 text-2xl font-bold text-ink tracking-tight">
          {formatValue(data.value, data.format)}
        </p>
      </div>

      {/* Mini sparkline area */}
      {data.sparklineData && data.sparklineData.length > 0 && (
        <div className="mt-3 flex items-end gap-0.5 h-8">
          {data.sparklineData.map((val, i) => {
            const max = Math.max(...data.sparklineData!);
            const height = max > 0 ? (val / max) * 100 : 0;
            return (
              <div
                key={i}
                className="flex-1 rounded-sm bg-blue-200/60 transition-all duration-300"
                style={{ height: `${Math.max(height, 4)}%` }}
              />
            );
          })}
        </div>
      )}
    </Card>
  );
}
