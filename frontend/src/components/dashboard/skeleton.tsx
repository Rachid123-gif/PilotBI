"use client";

import { Card } from "@/components/ui/card";

function Pulse({ className }: { className?: string }) {
  return (
    <div className={`rounded-lg bg-gray-100 animate-pulse ${className || ""}`} />
  );
}

export function KpiCardSkeleton() {
  return (
    <Card className="border-0 p-5 shadow-sm" style={{ borderTop: "3px solid #E2E8F0" }}>
      <div className="flex items-start justify-between">
        <Pulse className="h-11 w-11 rounded-xl" />
        <Pulse className="h-6 w-16 rounded-full" />
      </div>
      <div className="mt-4 space-y-2">
        <Pulse className="h-3.5 w-24" />
        <Pulse className="h-8 w-32" />
      </div>
      <div className="mt-4 flex items-end gap-[3px] h-10">
        {Array.from({ length: 12 }).map((_, i) => (
          <div
            key={i}
            className="flex-1 rounded-sm bg-gray-100 animate-pulse"
            style={{ height: `${20 + Math.random() * 60}%`, animationDelay: `${i * 50}ms` }}
          />
        ))}
      </div>
    </Card>
  );
}

export function ChartSkeleton() {
  return (
    <Card className="border-0 p-6 shadow-sm">
      <div className="flex items-center justify-between mb-5">
        <Pulse className="h-4 w-36" />
        <Pulse className="h-5 w-20 rounded-full" />
      </div>
      <div className="space-y-3">
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="flex items-end gap-2">
            <div className="h-3 w-8 rounded-lg bg-gray-100 animate-pulse" />
            <div
              className="flex-1 rounded bg-gray-100 animate-pulse"
              style={{ height: `${12 + Math.random() * 24}px`, animationDelay: `${i * 80}ms` }}
            />
          </div>
        ))}
      </div>
    </Card>
  );
}

export function InsightSkeleton() {
  return (
    <Card className="border-0 bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 p-5 sm:p-6 shadow-xl">
      <div className="flex items-start gap-4">
        <Pulse className="h-10 w-10 rounded-xl !bg-white/10" />
        <div className="flex-1 space-y-2">
          <Pulse className="h-3 w-20 !bg-white/10" />
          <Pulse className="h-3.5 w-3/4 !bg-white/10" />
          <Pulse className="h-3.5 w-1/2 !bg-white/10" />
        </div>
      </div>
    </Card>
  );
}

export function DashboardSkeleton() {
  return (
    <div className="space-y-6 animate-fade-in">
      <InsightSkeleton />
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <KpiCardSkeleton key={i} />
        ))}
      </div>
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <ChartSkeleton />
        <ChartSkeleton />
      </div>
    </div>
  );
}
