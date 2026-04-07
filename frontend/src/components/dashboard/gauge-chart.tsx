"use client";

import { Card } from "@/components/ui/card";

interface GaugeChartProps {
  title: string;
  value: number;
  unit?: string;
  min?: number;
  max?: number;
  thresholds?: { green: number; orange: number; red: number };
  className?: string;
}

export function GaugeChart({
  title,
  value,
  unit = "%",
  min = 0,
  max = 100,
  thresholds = { green: 30, orange: 50, red: 70 },
  className,
}: GaugeChartProps) {
  const range = max - min;
  const pct = Math.max(0, Math.min(100, ((value - min) / range) * 100));
  const angle = -90 + (pct / 100) * 180;

  const color =
    value <= thresholds.green
      ? "#10B981"
      : value <= thresholds.orange
        ? "#F59E0B"
        : "#EF4444";

  return (
    <Card className={`p-5 bg-white shadow-sm ${className || ""}`}>
      <p className="text-sm font-medium text-ink-3 mb-3">{title}</p>

      <div className="relative mx-auto" style={{ width: 160, height: 90 }}>
        <svg viewBox="0 0 160 90" className="w-full h-full">
          {/* Background arc */}
          <path
            d="M 15 80 A 65 65 0 0 1 145 80"
            fill="none"
            stroke="#E2E8F0"
            strokeWidth="12"
            strokeLinecap="round"
          />
          {/* Colored arc */}
          <path
            d="M 15 80 A 65 65 0 0 1 145 80"
            fill="none"
            stroke={color}
            strokeWidth="12"
            strokeLinecap="round"
            strokeDasharray={`${pct * 2.04} 204`}
            className="transition-all duration-700 ease-out"
          />
          {/* Needle */}
          <line
            x1="80"
            y1="80"
            x2={80 + 50 * Math.cos((angle * Math.PI) / 180)}
            y2={80 + 50 * Math.sin((angle * Math.PI) / 180)}
            stroke="#1E293B"
            strokeWidth="2.5"
            strokeLinecap="round"
            className="transition-all duration-700 ease-out"
          />
          <circle cx="80" cy="80" r="4" fill="#1E293B" />
        </svg>
      </div>

      <div className="text-center -mt-1">
        <span className="text-2xl font-bold text-ink" style={{ color }}>
          {value.toFixed(1)}
        </span>
        <span className="text-sm text-ink-3 ml-1">{unit}</span>
      </div>
    </Card>
  );
}
