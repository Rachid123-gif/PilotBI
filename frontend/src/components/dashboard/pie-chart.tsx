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

const BLUE_PALETTE = [
  "#2563EB",
  "#3B82F6",
  "#60A5FA",
  "#93C5FD",
  "#BFDBFE",
  "#DBEAFE",
];

function CustomTooltip({
  active,
  payload,
}: {
  active?: boolean;
  payload?: Array<{ name: string; value: number }>;
}) {
  if (!active || !payload?.[0]) return null;

  return (
    <div className="rounded-lg border border-border bg-white px-3 py-2 shadow-lg">
      <p className="text-xs font-medium text-ink-3">{payload[0].name}</p>
      <p className="text-sm font-bold text-ink">
        {new Intl.NumberFormat("fr-MA", {
          style: "currency",
          currency: "MAD",
          maximumFractionDigits: 0,
        }).format(payload[0].value)}
      </p>
    </div>
  );
}

export function DashboardPieChart({
  title,
  data,
  className,
}: DashboardPieChartProps) {
  const total = data.reduce((sum, item) => sum + item.value, 0);

  return (
    <Card className={`border-border/50 bg-white p-5 shadow-sm ${className}`}>
      <h3 className="mb-4 text-sm font-semibold text-ink">{title}</h3>
      <div className="flex items-center gap-6">
        <ResponsiveContainer width="50%" height={220}>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={55}
              outerRadius={85}
              paddingAngle={3}
              dataKey="value"
              stroke="none"
            >
              {data.map((_, index) => (
                <Cell
                  key={index}
                  fill={BLUE_PALETTE[index % BLUE_PALETTE.length]}
                />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
          </PieChart>
        </ResponsiveContainer>

        {/* Legend */}
        <div className="flex-1 space-y-2.5">
          {data.map((item, index) => {
            const percent = total > 0 ? ((item.value / total) * 100).toFixed(0) : 0;
            return (
              <div key={item.name} className="flex items-center gap-2">
                <div
                  className="h-2.5 w-2.5 rounded-full shrink-0"
                  style={{
                    backgroundColor:
                      BLUE_PALETTE[index % BLUE_PALETTE.length],
                  }}
                />
                <span className="flex-1 text-xs text-ink-3 truncate">
                  {item.name}
                </span>
                <span className="text-xs font-semibold text-ink tabular-nums">
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
