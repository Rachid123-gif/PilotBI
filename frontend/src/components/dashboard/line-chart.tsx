"use client";

import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer,
} from "recharts";
import { Card } from "@/components/ui/card";

interface LineChartData {
  label: string;
  value: number;
}

interface DashboardLineChartProps {
  title: string;
  data: LineChartData[];
  className?: string;
}

function CustomTooltip({ active, payload, label }: any) {
  if (!active || !payload?.[0]) return null;

  return (
    <div className="rounded-xl border-0 bg-gray-900 px-4 py-3 shadow-xl">
      <p className="text-[11px] font-medium text-gray-400 mb-0.5">{label}</p>
      <p className="text-base font-bold text-white tabular-nums">
        {new Intl.NumberFormat("fr-MA", {
          style: "currency", currency: "MAD", maximumFractionDigits: 0,
        }).format(payload[0].value)}
      </p>
    </div>
  );
}

export function DashboardLineChart({ title, data, className }: DashboardLineChartProps) {
  return (
    <Card className={`border-0 bg-white p-6 shadow-sm hover:shadow-md transition-shadow ${className || ""}`}>
      <div className="flex items-center justify-between mb-5">
        <h3 className="text-sm font-bold text-gray-900">{title}</h3>
        {data.length >= 2 && (
          <span className={`text-[11px] font-bold px-2.5 py-1 rounded-full ${
            data[data.length - 1].value >= data[data.length - 2].value
              ? "bg-emerald-50 text-emerald-700"
              : "bg-red-50 text-red-600"
          }`}>
            {data[data.length - 1].value >= data[data.length - 2].value ? "+" : ""}
            {(((data[data.length - 1].value - data[data.length - 2].value) / Math.abs(data[data.length - 2].value || 1)) * 100).toFixed(1)}%
          </span>
        )}
      </div>
      <ResponsiveContainer width="100%" height={280}>
        <AreaChart data={data} margin={{ top: 5, right: 5, bottom: 5, left: 5 }}>
          <defs>
            <linearGradient id="areaGradientPremium" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#3B82F6" stopOpacity={0.15} />
              <stop offset="50%" stopColor="#3B82F6" stopOpacity={0.05} />
              <stop offset="100%" stopColor="#3B82F6" stopOpacity={0} />
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
          <Tooltip content={<CustomTooltip />} />
          <Area
            type="monotone"
            dataKey="value"
            stroke="#2563EB"
            strokeWidth={2.5}
            fill="url(#areaGradientPremium)"
            dot={false}
            activeDot={{
              r: 6, fill: "#2563EB", stroke: "#fff", strokeWidth: 3,
            }}
          />
        </AreaChart>
      </ResponsiveContainer>
    </Card>
  );
}
