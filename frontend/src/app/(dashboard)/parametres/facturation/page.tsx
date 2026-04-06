"use client";

import Link from "next/link";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import {
  ArrowLeft,
  CheckCircle2,
  CreditCard,
  ExternalLink,
  Zap,
} from "lucide-react";
import {
  PLAN_NAMES,
  PLAN_PRICES,
  FEATURES,
  type PlanId,
} from "@/lib/constants";

const CURRENT_PLAN: PlanId = "starter";

const USAGE = {
  dataSources: { used: 1, limit: 1 },
  reports: { used: 2, limit: 3 },
  alerts: { used: 1, limit: 2 },
};

export default function FacturationPage() {
  return (
    <div className="mx-auto max-w-3xl space-y-6 animate-fade-in">
      <Link
        href="/parametres"
        className="inline-flex items-center text-sm text-ink-3 hover:text-ink transition-colors"
      >
        <ArrowLeft className="mr-1.5 h-4 w-4" />
        Parametres
      </Link>

      <div>
        <h1 className="text-2xl font-bold text-ink tracking-tight">
          Facturation
        </h1>
        <p className="mt-1 text-sm text-ink-3">
          Gerez votre abonnement et consultez votre consommation
        </p>
      </div>

      {/* Current plan */}
      <Card className="border-border/50 bg-white p-6 shadow-sm">
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-lg font-semibold text-ink">Plan actuel</h2>
              <Badge className="bg-blue-50 text-blue-700 border-blue-200" variant="outline">
                {PLAN_NAMES[CURRENT_PLAN]}
              </Badge>
            </div>
            <p className="mt-1 text-sm text-ink-3">
              {PLAN_PRICES[CURRENT_PLAN] === 0
                ? "Gratuit"
                : `${PLAN_PRICES[CURRENT_PLAN]} MAD / mois`}
            </p>
          </div>
          <Button variant="outline" size="sm">
            <ExternalLink className="mr-1.5 h-3.5 w-3.5" />
            Portail Stripe
          </Button>
        </div>

        <Separator className="my-4" />

        {/* Usage bars */}
        <div className="space-y-4">
          <h3 className="text-sm font-medium text-ink">Utilisation</h3>
          {Object.entries(USAGE).map(([key, { used, limit }]) => {
            const percent = (used / limit) * 100;
            const labels: Record<string, string> = {
              dataSources: "Sources de donnees",
              reports: "Rapports ce mois",
              alerts: "Alertes actives",
            };
            return (
              <div key={key}>
                <div className="flex items-center justify-between text-sm mb-1.5">
                  <span className="text-ink-2">{labels[key]}</span>
                  <span className="font-medium text-ink">
                    {used} / {limit}
                  </span>
                </div>
                <div className="h-2 w-full rounded-full bg-gray-100">
                  <div
                    className={`h-2 rounded-full transition-all ${
                      percent >= 90
                        ? "bg-red-500"
                        : percent >= 70
                          ? "bg-amber-500"
                          : "bg-blue-500"
                    }`}
                    style={{ width: `${Math.min(percent, 100)}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </Card>

      {/* Upgrade plans */}
      <div>
        <h2 className="mb-4 text-lg font-semibold text-ink">
          Mettre a niveau
        </h2>
        <div className="grid gap-4 sm:grid-cols-2">
          {(["pro", "equipe"] as PlanId[]).map((planId) => (
            <Card
              key={planId}
              className={`border-border/50 bg-white p-6 shadow-sm transition-all hover:shadow-md ${
                planId === "pro" ? "ring-2 ring-blue-600 ring-offset-2" : ""
              }`}
            >
              {planId === "pro" && (
                <Badge className="mb-3 bg-blue-600 text-white">
                  Recommande
                </Badge>
              )}
              <h3 className="text-lg font-bold text-ink">
                {PLAN_NAMES[planId]}
              </h3>
              <div className="mt-1">
                <span className="text-3xl font-bold text-ink">
                  {PLAN_PRICES[planId]}
                </span>
                <span className="text-sm text-ink-3"> MAD / mois</span>
              </div>

              <ul className="mt-4 space-y-2">
                {FEATURES[planId].map((feature) => (
                  <li
                    key={feature}
                    className="flex items-center gap-2 text-sm text-ink-2"
                  >
                    <CheckCircle2 className="h-4 w-4 shrink-0 text-blue-500" />
                    {feature}
                  </li>
                ))}
              </ul>

              <Button
                className={`mt-6 w-full ${
                  planId === "pro"
                    ? "bg-blue-600 hover:bg-blue-700 text-white"
                    : "bg-white text-ink border border-border hover:bg-gray-50"
                }`}
              >
                <Zap className="mr-2 h-4 w-4" />
                Passer au {PLAN_NAMES[planId]}
              </Button>
            </Card>
          ))}
        </div>
      </div>

      {/* Invoices */}
      <Card className="border-border/50 bg-white p-6 shadow-sm">
        <h3 className="text-sm font-semibold text-ink mb-3">
          Dernieres factures
        </h3>
        <div className="space-y-2">
          {[
            { date: "1 avril 2026", amount: "Gratuit", status: "Payee" },
            { date: "1 mars 2026", amount: "Gratuit", status: "Payee" },
            { date: "1 fevrier 2026", amount: "Gratuit", status: "Payee" },
          ].map((invoice, i) => (
            <div
              key={i}
              className="flex items-center justify-between rounded-lg bg-gray-50 px-4 py-3"
            >
              <div className="flex items-center gap-3">
                <CreditCard className="h-4 w-4 text-ink-3" />
                <span className="text-sm text-ink-2">{invoice.date}</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-sm font-medium text-ink">
                  {invoice.amount}
                </span>
                <Badge
                  variant="outline"
                  className="bg-emerald-50 text-emerald-700 border-emerald-200 text-xs"
                >
                  {invoice.status}
                </Badge>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
