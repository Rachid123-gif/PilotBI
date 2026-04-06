"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { DATA_SOURCE_TYPES } from "@/lib/constants";
import {
  ArrowRight,
  ArrowLeft,
  FileSpreadsheet,
  FileText,
  Sheet,
  Database as DatabaseIcon,
  Calculator,
} from "lucide-react";

const TYPE_ICONS: Record<string, React.ReactNode> = {
  excel: <FileSpreadsheet className="h-6 w-6" />,
  csv: <FileText className="h-6 w-6" />,
  google_sheets: <Sheet className="h-6 w-6" />,
  odoo: <DatabaseIcon className="h-6 w-6" />,
  sage: <Calculator className="h-6 w-6" />,
};

export default function OnboardingStep3() {
  const router = useRouter();
  const [selectedType, setSelectedType] = useState<string>("");

  function handleNext() {
    const prev = JSON.parse(sessionStorage.getItem("onboarding") || "{}");
    sessionStorage.setItem(
      "onboarding",
      JSON.stringify({ ...prev, dataSourceType: selectedType })
    );
    router.push("/onboarding/upload");
  }

  return (
    <div className="animate-fade-in">
      <div className="mb-8 text-center">
        <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-50">
          <DatabaseIcon className="h-7 w-7 text-blue-600" />
        </div>
        <h1 className="text-2xl font-bold text-ink">
          D&apos;ou viennent vos donnees ?
        </h1>
        <p className="mt-2 text-sm text-ink-3">
          Choisissez le format de votre source de donnees principale
        </p>
      </div>

      <div className="grid gap-3">
        {DATA_SOURCE_TYPES.map((type) => (
          <button
            key={type.id}
            type="button"
            onClick={() => setSelectedType(type.id)}
            className={cn(
              "flex items-center gap-4 rounded-xl border-2 p-4 text-left transition-all duration-200",
              selectedType === type.id
                ? "border-blue-600 bg-blue-50 shadow-sm"
                : "border-gray-200 bg-white hover:border-blue-200 hover:bg-blue-50/50"
            )}
          >
            <div
              className={cn(
                "flex h-12 w-12 items-center justify-center rounded-xl transition-colors",
                selectedType === type.id
                  ? "bg-blue-600 text-white"
                  : "bg-gray-50 text-ink-3"
              )}
            >
              {TYPE_ICONS[type.id]}
            </div>
            <div>
              <span
                className={cn(
                  "font-medium",
                  selectedType === type.id ? "text-blue-700" : "text-ink"
                )}
              >
                {type.label}
              </span>
              {(type.id === "odoo" || type.id === "sage") && (
                <span className="ml-2 inline-flex items-center rounded-full bg-amber-50 px-2 py-0.5 text-[10px] font-medium text-amber-700">
                  Bientot
                </span>
              )}
            </div>
          </button>
        ))}
      </div>

      <div className="mt-8 flex gap-3">
        <Button
          variant="outline"
          className="flex-1 h-11"
          onClick={() => router.push("/onboarding/secteur")}
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Retour
        </Button>
        <Button
          className="flex-1 bg-blue-600 hover:bg-blue-700 text-white h-11"
          disabled={!selectedType}
          onClick={handleNext}
        >
          Continuer
          <ArrowRight className="ml-2 h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}
