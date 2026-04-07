"use client";

import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";
import { Card } from "@/components/ui/card";

interface PieData {
  name: string;
  value: number;
}

interface DashboardPieChartProps {
  title: string;
  data: PieData[];
  className?: string;
}

const PALETTE = [
  "#2563EB", "#0891B2", "#7C3AED", "#059669", "#F59E0B",
  "#DC2626", "#0D9488", "#6366F1", "#EA580C", "#CA8A04",
];

function CustomTooltip({ active, payload }: any) {
  if (!active || !payload?.[0]) return null;

  return (
    <div className="rounded-xl border-0 bg-gray-900 px-4 py-3 shadow-xl">
      <p className="text-[11px] font-medium text-gray-400 mb-0.5">
        {payload[0].name}
      </p>
      <p className="text-base font-bold text-white tabular-nums">
        {new Intl.NumberFormat("fr-MA", {
          style: "currency", currency: "MAD", maximumFractionDigits: 0,
        }).format(payload[0].value)}
      </p>
    </div>
  );
}

export function DashboardPieChart({ title, data, className }: DashboardPieChartProps) {
  const total = data.reduce((sum, item) => sum + item.value, 0);
  const sorted = [...data].sort((a, b) => b.value - a.value);

  return (
    <Card className={`border-0 bg-white p-6 shadow-sm hover:shadow-md transition-shadow ${className || ""}`}>
      <h3 className="mb-5 text-sm font-bold text-gray-900">{title}</h3>
      <div className="flex items-center gap-6">
        <div className="relative" style={{ width: "45%", minWidth: 160 }}>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={sorted}
                cx="50%"
                cy="50%"
                innerRadius={52}
                outerRadius={82}
                paddingAngle={3}
                dataKey="value"
                stroke="none"
                animationBegin={0}
                animationDuration={800}
              >
                {sorted.map((_, index) => (
                  <Cell key={index} fill={PALETTE[index % PALETTE.length]} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
            </PieChart>
          </ResponsiveContainer>
          {/* Center total */}
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
            <div className="text-center">
              <p className="text-[10px] font-medium text-gray-400">Total</p>
              <p className="text-sm font-bold text-gray-900 tabular-nums">
                {total >= 1_000_000 ? `${(total / 1_000_000).toFixed(1)}M` : total >= 1_000 ? `${(total / 1_000).toFixed(0)}K` : total}
              </p>
            </div>
          </div>
        </div>

        {/* Legend */}
        <div className="flex-1 space-y-2">
          {sorted.map((item, index) => {
            const percent = total > 0 ? ((item.value / total) * 100).toFixed(0) : "0";
            return (
              <div key={item.name} className="flex items-center gap-2.5 group/item">
                <div
                  className="h-3 w-3 rounded-[3px] shrink-0 transition-transform group-hover/item:scale-125"
                  style={{ backgroundColor: PALETTE[index % PALETTE.length] }}
                />
                <span className="flex-1 text-[12px] text-gray-500 truncate">
                  {item.name}
                </span>
                <span className="text-[12px] font-bold text-gray-800 tabular-nums">
                  {percent}%
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </Card>
  );
}
