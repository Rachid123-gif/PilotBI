"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { SECTORS } from "@/lib/constants";
import {
  ArrowRight,
  ArrowLeft,
  Truck,
  ShoppingBag,
  Briefcase,
  Globe,
  MoreHorizontal,
} from "lucide-react";

const SECTOR_ICONS: Record<string, React.ReactNode> = {
  distribution: <Truck className="h-6 w-6" />,
  retail: <ShoppingBag className="h-6 w-6" />,
  services: <Briefcase className="h-6 w-6" />,
  import_export: <Globe className="h-6 w-6" />,
  autre: <MoreHorizontal className="h-6 w-6" />,
};

export default function OnboardingStep2() {
  const router = useRouter();
  const [selectedSector, setSelectedSector] = useState<string>("");

  function handleNext() {
    const prev = JSON.parse(sessionStorage.getItem("onboarding") || "{}");
    sessionStorage.setItem(
      "onboarding",
      JSON.stringify({ ...prev, sector: selectedSector })
    );
    router.push("/onboarding/donnees");
  }

  return (
    <div className="animate-fade-in">
      <div className="mb-8 text-center">
        <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-50">
          <Briefcase className="h-7 w-7 text-blue-600" />
        </div>
        <h1 className="text-2xl font-bold text-ink">
          Quel est votre secteur ?
        </h1>
        <p className="mt-2 text-sm text-ink-3">
          Nous adapterons les KPIs et rapports a votre activite
        </p>
      </div>

      <div className="grid gap-3">
        {SECTORS.map((sector) => (
          <button
            key={sector.id}
            type="button"
            onClick={() => setSelectedSector(sector.id)}
            className={cn(
              "flex items-center gap-4 rounded-xl border-2 p-4 text-left transition-all duration-200",
              selectedSector === sector.id
                ? "border-blue-600 bg-blue-50 shadow-sm"
                : "border-gray-200 bg-white hover:border-blue-200 hover:bg-blue-50/50"
            )}
          >
            <div
              className={cn(
                "flex h-12 w-12 items-center justify-center rounded-xl transition-colors",
                selectedSector === sector.id
                  ? "bg-blue-600 text-white"
                  : "bg-gray-50 text-ink-3"
              )}
            >
              {SECTOR_ICONS[sector.id]}
            </div>
            <span
              className={cn(
                "font-medium",
                selectedSector === sector.id ? "text-blue-700" : "text-ink"
              )}
            >
              {sector.label}
            </span>
          </button>
        ))}
      </div>

      <div className="mt-8 flex gap-3">
        <Button
          variant="outline"
          className="flex-1 h-11"
          onClick={() => router.push("/onboarding")}
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Retour
        </Button>
        <Button
          className="flex-1 bg-blue-600 hover:bg-blue-700 text-white h-11"
          disabled={!selectedSector}
          onClick={handleNext}
        >
          Continuer
          <ArrowRight className="ml-2 h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}
