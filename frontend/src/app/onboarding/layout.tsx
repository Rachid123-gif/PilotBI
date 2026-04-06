"use client";

import { usePathname } from "next/navigation";
import Link from "next/link";
import { cn } from "@/lib/utils";
import { Check } from "lucide-react";

const STEPS = [
  { path: "/onboarding", label: "Entreprise" },
  { path: "/onboarding/secteur", label: "Secteur" },
  { path: "/onboarding/donnees", label: "Donnees" },
  { path: "/onboarding/upload", label: "Import" },
  { path: "/onboarding/confirmation", label: "Confirmation" },
];

export default function OnboardingLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const currentStepIndex = STEPS.findIndex((s) => s.path === pathname);

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50/50 to-white">
      {/* Header */}
      <header className="border-b border-blue-100 bg-white/80 backdrop-blur-sm">
        <div className="mx-auto flex max-w-3xl items-center justify-between px-4 py-4">
          <Link href="/" className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-600">
              <svg
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                className="text-white"
              >
                <path
                  d="M3 13h4v8H3v-8Zm7-5h4v13h-4V8Zm7-5h4v18h-4V3Z"
                  fill="currentColor"
                />
              </svg>
            </div>
            <span className="text-lg font-bold text-ink">PilotBI</span>
          </Link>
          <span className="text-sm text-ink-3">
            Etape {currentStepIndex + 1} sur {STEPS.length}
          </span>
        </div>
      </header>

      {/* Progress Stepper */}
      <div className="mx-auto max-w-3xl px-4 pt-8 pb-4">
        <div className="flex items-center justify-between">
          {STEPS.map((step, index) => {
            const isActive = index === currentStepIndex;
            const isCompleted = index < currentStepIndex;

            return (
              <div key={step.path} className="flex flex-1 items-center">
                <div className="flex flex-col items-center gap-1.5">
                  <div
                    className={cn(
                      "flex h-9 w-9 items-center justify-center rounded-full border-2 text-sm font-medium transition-all duration-300",
                      isCompleted &&
                        "border-blue-600 bg-blue-600 text-white",
                      isActive &&
                        "border-blue-600 bg-blue-50 text-blue-600 ring-4 ring-blue-100",
                      !isActive &&
                        !isCompleted &&
                        "border-gray-200 bg-white text-ink-3"
                    )}
                  >
                    {isCompleted ? (
                      <Check className="h-4 w-4" />
                    ) : (
                      index + 1
                    )}
                  </div>
                  <span
                    className={cn(
                      "text-xs font-medium whitespace-nowrap",
                      isActive ? "text-blue-600" : "text-ink-3"
                    )}
                  >
                    {step.label}
                  </span>
                </div>
                {index < STEPS.length - 1 && (
                  <div
                    className={cn(
                      "mx-2 h-0.5 flex-1 rounded-full transition-all duration-500",
                      index < currentStepIndex
                        ? "bg-blue-600"
                        : "bg-gray-200"
                    )}
                  />
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Content */}
      <main className="mx-auto max-w-xl px-4 py-8">{children}</main>
    </div>
  );
}
