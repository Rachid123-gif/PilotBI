"use client";

import { Card } from "@/components/ui/card";
import { TrendingUp, TrendingDown } from "lucide-react";

interface RankingItem {
  name: string;
  value: number;
  change?: number;
}

interface RankingTableProps {
  title: string;
  items: RankingItem[];
  unit?: string;
  maxItems?: number;
  className?: string;
}

export function RankingTable({
  title,
  items,
  unit = "MAD",
  maxItems = 10,
  className,
}: RankingTableProps) {
  const sorted = [...items].sort((a, b) => b.value - a.value).slice(0, maxItems);
  const maxValue = sorted[0]?.value || 1;

  function formatValue(v: number): string {
    if (unit === "MAD") {
      return v >= 1000
        ? `${(v / 1000).toFixed(1)}K`
        : v.toFixed(0);
    }
    if (unit === "%") return `${v.toFixed(1)}%`;
    return v.toFixed(0);
  }

  return (
    <Card className={`p-5 bg-white shadow-sm ${className || ""}`}>
      <p className="text-sm font-medium text-ink-3 mb-4">{title}</p>

      <div className="space-y-2.5">
        {sorted.map((item, i) => {
          const barWidth = (item.value / maxValue) * 100;
          return (
            <div key={item.name} className="group">
              <div className="flex items-center justify-between mb-1">
                <div className="flex items-center gap-2 min-w-0">
                  <span className="text-xs font-bold text-ink-3 w-5 shrink-0">
                    {i + 1}
                  </span>
                  <span className="text-sm font-medium text-ink truncate">
                    {item.name}
                  </span>
                </div>
                <div className="flex items-center gap-2 shrink-0 ml-2">
                  <span className="text-sm font-semibold text-ink">
                    {formatValue(item.value)} {unit !== "MAD" && unit !== "%" ? unit : ""}
                    {unit === "MAD" && " MAD"}
                  </span>
                  {item.change !== undefined && item.change !== 0 && (
                    <span
                      className={`flex items-center text-xs font-medium ${
                        item.change > 0 ? "text-emerald-600" : "text-red-500"
                      }`}
                    >
                      {item.change > 0 ? (
                        <TrendingUp className="h-3 w-3 mr-0.5" />
                      ) : (
                        <TrendingDown className="h-3 w-3 mr-0.5" />
                      )}
                      {Math.abs(item.change).toFixed(0)}%
                    </span>
                  )}
                </div>
              </div>
              <div className="h-1.5 w-full rounded-full bg-gray-100 overflow-hidden">
                <div
                  className="h-full rounded-full bg-blue-500 transition-all duration-500 ease-out"
                  style={{ width: `${barWidth}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>

      {items.length > maxItems && (
        <p className="mt-3 text-center text-xs text-ink-3">
          +{items.length - maxItems} autres
        </p>
      )}
    </Card>
  );
}
