"use client";

import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Cell,
} from "recharts";
import { Card } from "@/components/ui/card";

interface BarChartData {
  label: string;
  value: number;
}

interface DashboardBarChartProps {
  title: string;
  data: BarChartData[];
  className?: string;
}

function CustomTooltip({ active, payload, label }: any) {
  if (!active || !payload?.[0]) return null;
  const value = payload[0].value;

  return (
    <div className="rounded-xl border-0 bg-gray-900 px-4 py-3 shadow-xl">
      <p className="text-[11px] font-medium text-gray-400 mb-0.5">{label}</p>
      <p className="text-base font-bold text-white tabular-nums">
        {new Intl.NumberFormat("fr-MA", {
          style: "currency", currency: "MAD", maximumFractionDigits: 0,
        }).format(value)}
      </p>
    </div>
  );
}

export function DashboardBarChart({ title, data, className }: DashboardBarChartProps) {
  const maxVal = Math.max(...data.map((d) => d.value));

  return (
    <Card className={`border-0 bg-white p-6 shadow-sm hover:shadow-md transition-shadow ${className || ""}`}>
      <div className="flex items-center justify-between mb-5">
        <h3 className="text-sm font-bold text-gray-900">{title}</h3>
        <span className="text-[11px] font-medium text-gray-400 bg-gray-50 px-2.5 py-1 rounded-full">
          {data.length} periodes
        </span>
      </div>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data} margin={{ top: 5, right: 5, bottom: 5, left: 5 }}>
          <defs>
            <linearGradient id="barGradientPremium" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#3B82F6" />
              <stop offset="100%" stopColor="#1D4ED8" />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" vertical={false} />
          <XAxis
            dataKey="label"
            axisLine={false}
            tickLine={false}
            tick={{ fill: "#94A3B8", fontSize: 11, fontWeight: 500 }}
            dy={8}
          />
          <YAxis
            axisLine={false}
            tickLine={false}
            tick={{ fill: "#94A3B8", fontSize: 11 }}
            tickFormatter={(val: number) =>
              val >= 1_000_000 ? `${(val / 1_000_000).toFixed(1)}M`
              : val >= 1_000 ? `${(val / 1_000).toFixed(0)}k`
              : String(val)
            }
            width={50}
          />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: "rgba(37,99,235,0.04)", radius: 6 }} />
          <Bar dataKey="value" radius={[8, 8, 0, 0]} maxBarSize={44}>
            {data.map((entry, i) => (
              <Cell
                key={i}
                fill={entry.value === maxVal ? "url(#barGradientPremium)" : "#BFDBFE"}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </Card>
  );
}
