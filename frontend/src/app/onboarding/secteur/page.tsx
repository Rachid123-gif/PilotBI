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
  Store,
  Factory,
  UtensilsCrossed,
  ShoppingCart,
  HeartPulse,
  Pill,
  Building2,
  Hotel,
  Briefcase,
  Sprout,
} from "lucide-react";

const SECTOR_ICONS: Record<string, React.ReactNode> = {
  distribution: <Truck className="h-5 w-5" />,
  retail: <Store className="h-5 w-5" />,
  industrie: <Factory className="h-5 w-5" />,
  transport: <Truck className="h-5 w-5" />,
  restaurant: <UtensilsCrossed className="h-5 w-5" />,
  ecommerce: <ShoppingCart className="h-5 w-5" />,
  clinique: <HeartPulse className="h-5 w-5" />,
  pharmacie: <Pill className="h-5 w-5" />,
  immobilier: <Building2 className="h-5 w-5" />,
  hotel: <Hotel className="h-5 w-5" />,
  services: <Briefcase className="h-5 w-5" />,
  agriculture: <Sprout className="h-5 w-5" />,
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
      <div className="mb-6 text-center">
        <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-50">
          <Briefcase className="h-6 w-6 text-blue-600" />
        </div>
        <h1 className="text-2xl font-bold text-ink">
          Quel est votre secteur ?
        </h1>
        <p className="mt-1.5 text-sm text-ink-3">
          Votre dashboard sera personnalise avec les KPIs de votre metier
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 max-h-[420px] overflow-y-auto pr-1">
        {SECTORS.map((sector) => (
          <button
            key={sector.id}
            type="button"
            onClick={() => setSelectedSector(sector.id)}
            className={cn(
              "flex items-start gap-3 rounded-xl border-2 p-3.5 text-left transition-all duration-200",
              selectedSector === sector.id
                ? "border-blue-600 bg-blue-50 shadow-sm"
                : "border-gray-100 bg-white hover:border-blue-200 hover:bg-blue-50/30"
            )}
          >
            <div
              className={cn(
                "flex h-9 w-9 shrink-0 items-center justify-center rounded-lg transition-colors",
                selectedSector === sector.id
                  ? "bg-blue-600 text-white"
                  : "bg-gray-50 text-ink-3"
              )}
            >
              {SECTOR_ICONS[sector.id]}
            </div>
            <div className="min-w-0">
              <p
                className={cn(
                  "text-sm font-semibold leading-tight",
                  selectedSector === sector.id ? "text-blue-700" : "text-ink"
                )}
              >
                {sector.label}
              </p>
              <p className="mt-0.5 text-xs text-ink-3 leading-snug">
                {sector.description}
              </p>
            </div>
          </button>
        ))}
      </div>

      <div className="mt-6 flex gap-3">
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
