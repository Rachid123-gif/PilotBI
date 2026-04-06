"use client";

import Link from "next/link";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  FileBarChart,
  Download,
  Eye,
  Sparkles,
  Calendar,
} from "lucide-react";

const DEMO_REPORTS = [
  {
    id: "r1",
    title: "Rapport mensuel - Mars 2026",
    period: "Mars 2026",
    status: "ready" as const,
    generatedAt: "2026-04-01",
    summary:
      "Croissance de 8.9% du CA. Marge en hausse. 3 anomalies detectees dans les depenses logistiques.",
  },
  {
    id: "r2",
    title: "Rapport mensuel - Fevrier 2026",
    period: "Fevrier 2026",
    status: "ready" as const,
    generatedAt: "2026-03-01",
    summary:
      "CA stable a 2.12M MAD. Hausse notable des clients actifs (+15 nouveaux comptes B2B).",
  },
  {
    id: "r3",
    title: "Rapport mensuel - Janvier 2026",
    period: "Janvier 2026",
    status: "ready" as const,
    generatedAt: "2026-02-01",
    summary:
      "Demarrage d'annee solide. Stock optimise. Recommandation: renforcer l'approvisionnement boissons.",
  },
  {
    id: "r4",
    title: "Rapport trimestriel - Q4 2025",
    period: "Q4 2025",
    status: "ready" as const,
    generatedAt: "2026-01-05",
    summary:
      "Meilleur trimestre de l'annee. CA cumule: 8.55M MAD. Objectifs annuels atteints a 102%.",
  },
  {
    id: "r5",
    title: "Rapport mensuel - Avril 2026",
    period: "Avril 2026",
    status: "generating" as const,
    generatedAt: null,
    summary: null,
  },
];

const STATUS_CONFIG = {
  ready: { label: "Pret", className: "bg-emerald-50 text-emerald-700 border-emerald-200" },
  generating: {
    label: "En cours",
    className: "bg-amber-50 text-amber-700 border-amber-200",
  },
  draft: { label: "Brouillon", className: "bg-gray-50 text-ink-3 border-gray-200" },
  error: { label: "Erreur", className: "bg-red-50 text-red-700 border-red-200" },
};

export default function RapportsPage() {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-ink tracking-tight">
            Rapports
          </h1>
          <p className="mt-1 text-sm text-ink-3">
            Rapports d&apos;analyse generes automatiquement
          </p>
        </div>
        <Button className="bg-blue-600 hover:bg-blue-700 text-white">
          <Sparkles className="mr-2 h-4 w-4" />
          Generer un rapport
        </Button>
      </div>

      <div className="grid gap-4">
        {DEMO_REPORTS.map((report) => {
          const status = STATUS_CONFIG[report.status];
          return (
            <Card
              key={report.id}
              className="border-border/50 bg-white p-5 shadow-sm hover:shadow-md transition-all duration-200"
            >
              <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                <div className="flex items-start gap-4 min-w-0">
                  <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-blue-50">
                    <FileBarChart className="h-5 w-5 text-blue-600" />
                  </div>
                  <div className="min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <h3 className="font-semibold text-ink truncate">
                        {report.title}
                      </h3>
                      <Badge
                        variant="outline"
                        className={status.className}
                      >
                        {status.label}
                      </Badge>
                    </div>
                    {report.summary && (
                      <p className="mt-1.5 text-sm text-ink-3 line-clamp-2">
                        {report.summary}
                      </p>
                    )}
                    {report.generatedAt && (
                      <p className="mt-2 flex items-center gap-1 text-xs text-ink-3">
                        <Calendar className="h-3 w-3" />
                        Genere le{" "}
                        {new Date(report.generatedAt).toLocaleDateString(
                          "fr-FR",
                          {
                            year: "numeric",
                            month: "long",
                            day: "numeric",
                          }
                        )}
                      </p>
                    )}
                    {report.status === "generating" && (
                      <p className="mt-2 text-xs text-amber-600 flex items-center gap-1.5">
                        <span className="h-1.5 w-1.5 rounded-full bg-amber-500 animate-pulse-soft" />
                        Generation en cours...
                      </p>
                    )}
                  </div>
                </div>

                {report.status === "ready" && (
                  <div className="flex gap-2 shrink-0">
                    <Button
                      variant="outline"
                      size="sm"
                      render={<Link href={`/rapports/${report.id}`} />}
                    >
                      <Eye className="mr-1.5 h-3.5 w-3.5" />
                      Voir
                    </Button>
                    <Button variant="outline" size="sm">
                      <Download className="mr-1.5 h-3.5 w-3.5" />
                      PDF
                    </Button>
                  </div>
                )}
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
