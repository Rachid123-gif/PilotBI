"use client";

import { Card } from "@/components/ui/card";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";

interface ComparisonItem {
  name: string;
  value: number;
}

interface ComparisonChartProps {
  title: string;
  data: ComparisonItem[];
  unit?: string;
  color?: string;
  className?: string;
}

const COLORS = [
  "#2563EB", "#0891B2", "#7C3AED", "#15803D", "#F59E0B",
  "#DC2626", "#0D9488", "#CA8A04", "#6366F1", "#EA580C",
];

function CustomTooltip({ active, payload, label }: any) {
  if (!active || !payload?.length) return null;
  return (
    <div className="rounded-lg border bg-white px-3 py-2 shadow-md">
      <p className="text-xs font-medium text-ink">{label}</p>
      <p className="text-sm font-bold text-blue-600">
        {payload[0].value.toLocaleString("fr-MA")} MAD
      </p>
    </div>
  );
}

export function ComparisonChart({
  title,
  data,
  unit = "MAD",
  className,
}: ComparisonChartProps) {
  const sorted = [...data].sort((a, b) => b.value - a.value);

  return (
    <Card className={`p-5 bg-white shadow-sm ${className || ""}`}>
      <p className="text-sm font-medium text-ink-3 mb-4">{title}</p>
      <ResponsiveContainer width="100%" height={Math.max(200, sorted.length * 36)}>
        <BarChart data={sorted} layout="vertical" margin={{ left: 0, right: 20 }}>
          <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#F1F5F9" />
          <XAxis
            type="number"
            tick={{ fontSize: 11, fill: "#94A3B8" }}
            tickFormatter={(v: number) => v >= 1000 ? `${(v / 1000).toFixed(0)}K` : String(v)}
          />
          <YAxis
            type="category"
            dataKey="name"
            tick={{ fontSize: 11, fill: "#334155" }}
            width={90}
          />
          <Tooltip content={<CustomTooltip />} />
          <Bar dataKey="value" radius={[0, 4, 4, 0]} barSize={20}>
            {sorted.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </Card>
  );
}
