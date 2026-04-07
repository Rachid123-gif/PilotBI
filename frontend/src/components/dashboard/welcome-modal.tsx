"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Sparkles, BarChart3, Zap, ArrowRight, X } from "lucide-react";

interface WelcomeModalProps {
  sectorLabel?: string;
  onDismiss: () => void;
}

export function WelcomeModal({ sectorLabel, onDismiss }: WelcomeModalProps) {
  const [step, setStep] = useState<"loading" | "ready">("loading");

  useEffect(() => {
    const timer = setTimeout(() => setStep("ready"), 2500);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm animate-fade-in">
      <div className="relative mx-4 w-full max-w-md rounded-2xl bg-white p-8 shadow-2xl">
        <button
          onClick={onDismiss}
          className="absolute right-4 top-4 text-ink-3 hover:text-ink transition-colors"
        >
          <X className="h-5 w-5" />
        </button>

        {step === "loading" ? (
          <div className="text-center py-8">
            <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-50">
              <Sparkles className="h-8 w-8 text-blue-600 animate-pulse" />
            </div>
            <h2 className="text-xl font-bold text-ink">
              Analyse de vos donnees...
            </h2>
            <p className="mt-2 text-sm text-ink-3">
              Notre IA configure votre dashboard
              {sectorLabel ? ` ${sectorLabel}` : ""}
            </p>
            <div className="mt-6 flex justify-center gap-1.5">
              {[0, 1, 2].map((i) => (
                <div
                  key={i}
                  className="h-2 w-2 rounded-full bg-blue-400 animate-pulse"
                  style={{ animationDelay: `${i * 300}ms` }}
                />
              ))}
            </div>
          </div>
        ) : (
          <div className="text-center">
            <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-2xl bg-emerald-50">
              <Zap className="h-8 w-8 text-emerald-600" />
            </div>
            <h2 className="text-xl font-bold text-ink">
              Votre dashboard est pret !
            </h2>
            <p className="mt-2 text-sm text-ink-3">
              Personnalise pour{" "}
              {sectorLabel || "votre activite"}
            </p>

            <div className="mt-6 space-y-3 text-left">
              {[
                { icon: BarChart3, text: "KPIs adaptes a votre metier" },
                { icon: Sparkles, text: "Analyse IA de vos donnees" },
                { icon: Zap, text: "Alertes pre-configurees" },
              ].map(({ icon: Icon, text }, i) => (
                <div
                  key={i}
                  className="flex items-center gap-3 rounded-lg bg-gray-50 p-3"
                >
                  <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-50">
                    <Icon className="h-4 w-4 text-blue-600" />
                  </div>
                  <span className="text-sm font-medium text-ink">{text}</span>
                </div>
              ))}
            </div>

            <Button
              onClick={onDismiss}
              className="mt-6 w-full bg-blue-600 hover:bg-blue-700 text-white h-11 text-sm font-semibold"
            >
              Decouvrir mon dashboard
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
