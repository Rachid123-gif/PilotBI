"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { CheckCircle2, Rocket, ArrowRight } from "lucide-react";

export default function OnboardingStep5() {
  const router = useRouter();
  const [showContent, setShowContent] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setShowContent(true), 300);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="text-center">
      {/* Animated check */}
      <div
        className={`transition-all duration-700 ${
          showContent
            ? "opacity-100 scale-100"
            : "opacity-0 scale-75"
        }`}
      >
        <div className="mx-auto mb-6 flex h-24 w-24 items-center justify-center rounded-full bg-gradient-to-br from-blue-500 to-blue-700 shadow-lg shadow-blue-500/30">
          <CheckCircle2 className="h-12 w-12 text-white" />
        </div>
      </div>

      <div
        className={`transition-all duration-700 delay-300 ${
          showContent
            ? "opacity-100 translate-y-0"
            : "opacity-0 translate-y-4"
        }`}
      >
        <h1 className="text-3xl font-bold text-ink">
          Felicitations !
        </h1>
        <p className="mt-3 text-lg text-ink-2">
          Votre espace PilotBI est en cours de preparation
        </p>
      </div>

      <div
        className={`mt-8 rounded-2xl border border-blue-100 bg-blue-50 p-6 transition-all duration-700 delay-500 ${
          showContent
            ? "opacity-100 translate-y-0"
            : "opacity-0 translate-y-4"
        }`}
      >
        <div className="flex items-center justify-center gap-3 text-blue-700">
          <Rocket className="h-5 w-5" />
          <span className="font-semibold">
            Votre dashboard est pret !
          </span>
        </div>
        <p className="mt-2 text-sm text-blue-600">
          Vos donnees ont ete analysees et vos KPIs sont configures.
          Cliquez ci-dessous pour decouvrir votre tableau de bord.
        </p>
      </div>

      {/* Steps recap */}
      <div
        className={`mt-8 space-y-3 transition-all duration-700 delay-700 ${
          showContent
            ? "opacity-100 translate-y-0"
            : "opacity-0 translate-y-4"
        }`}
      >
        <div className="flex items-center gap-3 rounded-xl bg-gray-50 p-3 text-left">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-green-100">
            <CheckCircle2 className="h-4 w-4 text-green-600" />
          </div>
          <span className="text-sm text-ink-2">
            Profil entreprise configure
          </span>
        </div>
        <div className="flex items-center gap-3 rounded-xl bg-gray-50 p-3 text-left">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-green-100">
            <CheckCircle2 className="h-4 w-4 text-green-600" />
          </div>
          <span className="text-sm text-ink-2">
            Secteur d&apos;activite defini
          </span>
        </div>
        <div className="flex items-center gap-3 rounded-xl bg-gray-50 p-3 text-left">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100">
            <div className="h-2 w-2 rounded-full bg-blue-600 animate-pulse-soft" />
          </div>
          <span className="text-sm text-ink-2">
            Analyse des donnees en cours...
          </span>
        </div>
      </div>

      <Button
        className="mt-10 w-full bg-blue-600 hover:bg-blue-700 text-white h-12 text-base"
        onClick={() => router.push("/tableau-de-bord")}
      >
        Acceder a mon tableau de bord
        <ArrowRight className="ml-2 h-5 w-5" />
      </Button>
    </div>
  );
}
