"use client";

import { PERIODS, type PeriodId } from "@/lib/constants";
import { cn } from "@/lib/utils";

interface PeriodFilterProps {
  value: PeriodId;
  onChange: (period: PeriodId) => void;
}

export function PeriodFilter({ value, onChange }: PeriodFilterProps) {
  return (
    <div className="flex flex-wrap items-center gap-1 rounded-xl bg-gray-100 p-1">
      {PERIODS.filter((p) => p.id !== "custom").map((period) => (
        <button
          key={period.id}
          type="button"
          onClick={() => onChange(period.id)}
          className={cn(
            "rounded-lg px-3 py-1.5 text-xs font-medium transition-all duration-200",
            value === period.id
              ? "bg-white text-blue-700 shadow-sm"
              : "text-ink-3 hover:text-ink"
          )}
        >
          {period.label}
        </button>
      ))}
    </div>
  );
}
