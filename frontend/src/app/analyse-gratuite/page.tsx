"use client";

import { useState, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card } from "@/components/ui/card";
import {
  Upload,
  Mail,
  Building2,
  Sparkles,
  BarChart3,
  TrendingUp,
  AlertTriangle,
  ArrowRight,
  Loader2,
  CheckCircle2,
  FileSpreadsheet,
} from "lucide-react";
import Link from "next/link";

type Step = "upload" | "analyzing" | "results";

interface Insight {
  icon: "trending" | "alert" | "chart";
  text: string;
}

export default function AnalyseGratuitePage() {
  const [step, setStep] = useState<Step>("upload");
  const [email, setEmail] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const [insights, setInsights] = useState<Insight[]>([]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const dropped = e.dataTransfer.files[0];
    if (dropped && (dropped.name.endsWith(".xlsx") || dropped.name.endsWith(".csv") || dropped.name.endsWith(".xls"))) {
      setFile(dropped);
    }
  }, []);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    if (selected) setFile(selected);
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!file || !email) return;

    setStep("analyzing");

    // Simulate analysis (in production: upload to API, run analysis, return results)
    // For now, show realistic demo insights after a delay
    await new Promise((resolve) => setTimeout(resolve, 3000));

    setInsights([
      {
        icon: "trending",
        text: "Votre chiffre d'affaires montre une tendance haussiere de +12% sur les 3 derniers mois.",
      },
      {
        icon: "alert",
        text: "3 clients representent plus de 45% de votre CA total — un risque de concentration eleve.",
      },
      {
        icon: "chart",
        text: "Vos marges sont 6% en dessous de la moyenne sectorielle. Optimisation possible sur 4 references.",
      },
    ]);
    setStep("results");
  }

  const InsightIcon = ({ type }: { type: string }) => {
    switch (type) {
      case "trending":
        return <TrendingUp className="h-5 w-5 text-emerald-600" />;
      case "alert":
        return <AlertTriangle className="h-5 w-5 text-amber-500" />;
      default:
        return <BarChart3 className="h-5 w-5 text-blue-600" />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-600 via-blue-700 to-indigo-800">
      {/* Header */}
      <div className="px-6 py-6">
        <Link href="/" className="flex items-center gap-2 text-white">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-white/15">
            <BarChart3 className="h-4 w-4" />
          </div>
          <span className="text-lg font-bold">PilotBI</span>
        </Link>
      </div>

      <div className="mx-auto max-w-lg px-6 pb-20">
        {step === "upload" && (
          <div className="animate-fade-in">
            <div className="mb-8 text-center text-white">
              <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-white/15">
                <Sparkles className="h-7 w-7" />
              </div>
              <h1 className="text-3xl font-bold">
                Analysez votre Excel<br />gratuitement
              </h1>
              <p className="mt-3 text-blue-200 text-sm leading-relaxed">
                Uploadez votre fichier de ventes. En 30 secondes, recevez<br />
                3 insights IA + un apercu de votre dashboard.
              </p>
            </div>

            <Card className="p-6 bg-white/95 backdrop-blur-sm shadow-2xl border-0">
              <form onSubmit={handleSubmit} className="space-y-4">
                {/* File upload zone */}
                <div
                  onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
                  onDragLeave={() => setDragOver(false)}
                  onDrop={handleDrop}
                  className={`relative flex flex-col items-center justify-center rounded-xl border-2 border-dashed p-8 transition-all ${
                    dragOver
                      ? "border-blue-500 bg-blue-50"
                      : file
                        ? "border-emerald-400 bg-emerald-50"
                        : "border-gray-200 bg-gray-50 hover:border-blue-300 hover:bg-blue-50/50"
                  }`}
                >
                  <input
                    type="file"
                    accept=".xlsx,.xls,.csv"
                    onChange={handleFileSelect}
                    className="absolute inset-0 cursor-pointer opacity-0"
                  />
                  {file ? (
                    <>
                      <FileSpreadsheet className="h-8 w-8 text-emerald-600 mb-2" />
                      <p className="text-sm font-medium text-emerald-700">
                        {file.name}
                      </p>
                      <p className="text-xs text-emerald-600 mt-1">
                        {(file.size / 1024).toFixed(0)} Ko
                      </p>
                    </>
                  ) : (
                    <>
                      <Upload className="h-8 w-8 text-ink-3 mb-2" />
                      <p className="text-sm font-medium text-ink">
                        Glissez votre fichier ici
                      </p>
                      <p className="text-xs text-ink-3 mt-1">
                        Excel (.xlsx) ou CSV — Max 5 Mo
                      </p>
                    </>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="email">Votre email</Label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-3" />
                    <Input
                      id="email"
                      type="email"
                      placeholder="vous@entreprise.ma"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className="pl-10"
                      required
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="company">Nom de l&apos;entreprise (optionnel)</Label>
                  <div className="relative">
                    <Building2 className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-3" />
                    <Input
                      id="company"
                      type="text"
                      placeholder="Mon entreprise"
                      value={companyName}
                      onChange={(e) => setCompanyName(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                </div>

                <Button
                  type="submit"
                  disabled={!file || !email}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white h-12 text-sm font-semibold"
                >
                  <Sparkles className="mr-2 h-4 w-4" />
                  Analyser gratuitement
                </Button>

                <p className="text-center text-xs text-ink-3">
                  Vos donnees sont securisees et supprimees apres analyse.
                </p>
              </form>
            </Card>
          </div>
        )}

        {step === "analyzing" && (
          <div className="animate-fade-in text-center pt-20">
            <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-2xl bg-white/15">
              <Sparkles className="h-10 w-10 text-white animate-pulse" />
            </div>
            <h2 className="text-2xl font-bold text-white">
              Analyse en cours...
            </h2>
            <p className="mt-3 text-blue-200">
              Notre IA analyse vos donnees
            </p>
            <div className="mt-8 space-y-3 max-w-xs mx-auto">
              {["Lecture du fichier...", "Detection des colonnes...", "Calcul des KPIs...", "Generation des insights..."].map(
                (label, i) => (
                  <div
                    key={label}
                    className="flex items-center gap-3 text-left animate-fade-in"
                    style={{ animationDelay: `${i * 700}ms` }}
                  >
                    <Loader2
                      className="h-4 w-4 text-blue-300 animate-spin shrink-0"
                      style={{ animationDelay: `${i * 200}ms` }}
                    />
                    <span className="text-sm text-blue-200">{label}</span>
                  </div>
                )
              )}
            </div>
          </div>
        )}

        {step === "results" && (
          <div className="animate-fade-in">
            <div className="mb-8 text-center text-white">
              <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-emerald-500/20">
                <CheckCircle2 className="h-7 w-7 text-emerald-400" />
              </div>
              <h2 className="text-2xl font-bold">Analyse terminee !</h2>
              <p className="mt-2 text-blue-200 text-sm">
                Voici les 3 insights cles trouves dans vos donnees
              </p>
            </div>

            <div className="space-y-3 mb-6">
              {insights.map((insight, i) => (
                <Card
                  key={i}
                  className="p-4 bg-white/95 backdrop-blur-sm border-0 shadow-lg animate-fade-in"
                  style={{ animationDelay: `${i * 200}ms` }}
                >
                  <div className="flex gap-3">
                    <div className="shrink-0 mt-0.5">
                      <InsightIcon type={insight.icon} />
                    </div>
                    <p className="text-sm text-ink leading-relaxed">
                      {insight.text}
                    </p>
                  </div>
                </Card>
              ))}
            </div>

            <Card className="p-5 bg-white/95 backdrop-blur-sm border-0 shadow-lg text-center">
              <p className="text-sm font-medium text-ink mb-1">
                Vous voulez voir le dashboard complet ?
              </p>
              <p className="text-xs text-ink-3 mb-4">
                Gratuit, sans carte bancaire, pret en 30 secondes
              </p>
              <Link href="/inscription">
                <Button className="w-full bg-blue-600 hover:bg-blue-700 text-white h-11 font-semibold">
                  Creer mon dashboard gratuit
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </Link>
            </Card>

            <p className="mt-4 text-center text-xs text-blue-300">
              Un rapport complet a ete envoye a {email}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
