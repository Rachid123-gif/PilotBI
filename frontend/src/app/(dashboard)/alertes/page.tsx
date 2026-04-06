"use client";

import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Bell,
  Plus,
  TrendingDown,
  TrendingUp,
  AlertTriangle,
  DollarSign,
  Package,
  Users,
  Clock,
  CheckCircle2,
} from "lucide-react";

interface DemoAlert {
  id: string;
  name: string;
  kpiType: string;
  condition: string;
  threshold: number;
  isActive: boolean;
  icon: React.ReactNode;
}

const DEMO_ALERTS: DemoAlert[] = [
  {
    id: "a1",
    name: "CA inferieur a 2M MAD",
    kpiType: "Chiffre d'affaires",
    condition: "Inferieur a",
    threshold: 2_000_000,
    isActive: true,
    icon: <DollarSign className="h-4 w-4" />,
  },
  {
    id: "a2",
    name: "Marge nette sous 10%",
    kpiType: "Marge nette",
    condition: "Inferieur a",
    threshold: 10,
    isActive: true,
    icon: <TrendingDown className="h-4 w-4" />,
  },
  {
    id: "a3",
    name: "Stock critique > 10 articles",
    kpiType: "Stock critique",
    condition: "Superieur a",
    threshold: 10,
    isActive: true,
    icon: <Package className="h-4 w-4" />,
  },
  {
    id: "a4",
    name: "Perte de clients > 5%",
    kpiType: "Clients actifs",
    condition: "Baisse superieure a",
    threshold: 5,
    isActive: false,
    icon: <Users className="h-4 w-4" />,
  },
];

const DEMO_HISTORY = [
  {
    id: "h1",
    alertName: "Stock critique > 10 articles",
    message: "12 articles sont en stock critique. Risque de rupture imminent.",
    value: 12,
    triggeredAt: "2026-04-05T14:30:00",
    isRead: false,
  },
  {
    id: "h2",
    alertName: "CA inferieur a 2M MAD",
    message:
      "Le CA du mois d'aout 2025 etait de 1.87M MAD, sous le seuil de 2M.",
    value: 1_870_000,
    triggeredAt: "2025-09-01T09:00:00",
    isRead: true,
  },
  {
    id: "h3",
    alertName: "Marge nette sous 10%",
    message: "Marge nette a 9.2% en juin 2025. En dessous du seuil de 10%.",
    value: 9.2,
    triggeredAt: "2025-07-01T09:00:00",
    isRead: true,
  },
];

export default function AlertesPage() {
  const [alerts, setAlerts] = useState(DEMO_ALERTS);
  const [dialogOpen, setDialogOpen] = useState(false);

  function toggleAlert(id: string) {
    setAlerts((prev) =>
      prev.map((a) =>
        a.id === id ? { ...a, isActive: !a.isActive } : a
      )
    );
  }

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-ink tracking-tight">
            Alertes
          </h1>
          <p className="mt-1 text-sm text-ink-3">
            Configurez des alertes sur vos KPIs
          </p>
        </div>
        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
          <DialogTrigger
            render={
              <Button className="bg-blue-600 hover:bg-blue-700 text-white" />
            }
          >
            <Plus className="mr-2 h-4 w-4" />
            Nouvelle alerte
          </DialogTrigger>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle>Creer une alerte</DialogTitle>
            </DialogHeader>
            <div className="space-y-4 pt-2">
              <div className="space-y-2">
                <Label>Nom de l&apos;alerte</Label>
                <Input placeholder="Ex: CA inferieur a 2M" />
              </div>
              <div className="space-y-2">
                <Label>KPI</Label>
                <select className="flex h-10 w-full rounded-lg border border-input bg-background px-3 text-sm">
                  <option>Chiffre d&apos;affaires</option>
                  <option>Marge nette</option>
                  <option>Clients actifs</option>
                  <option>Stock critique</option>
                </select>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="space-y-2">
                  <Label>Condition</Label>
                  <select className="flex h-10 w-full rounded-lg border border-input bg-background px-3 text-sm">
                    <option>Superieur a</option>
                    <option>Inferieur a</option>
                    <option>Hausse superieure a</option>
                    <option>Baisse superieure a</option>
                  </select>
                </div>
                <div className="space-y-2">
                  <Label>Seuil</Label>
                  <Input type="number" placeholder="Valeur" />
                </div>
              </div>
              <Button
                className="w-full bg-blue-600 hover:bg-blue-700 text-white"
                onClick={() => setDialogOpen(false)}
              >
                Creer l&apos;alerte
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      {/* Active alerts */}
      <div>
        <h2 className="mb-3 text-sm font-semibold text-ink-3 uppercase tracking-wider">
          Alertes configurees
        </h2>
        <div className="grid gap-3">
          {alerts.map((alert) => (
            <Card
              key={alert.id}
              className="border-border/50 bg-white p-4 shadow-sm"
            >
              <div className="flex items-center gap-4">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-blue-600">
                  {alert.icon}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-ink truncate">{alert.name}</p>
                  <p className="text-xs text-ink-3">
                    {alert.kpiType} &middot; {alert.condition}{" "}
                    {alert.threshold.toLocaleString("fr-FR")}
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => toggleAlert(alert.id)}
                  className={`relative h-6 w-11 rounded-full transition-colors ${
                    alert.isActive ? "bg-blue-600" : "bg-gray-200"
                  }`}
                >
                  <span
                    className={`absolute top-0.5 left-0.5 h-5 w-5 rounded-full bg-white shadow transition-transform ${
                      alert.isActive ? "translate-x-5" : "translate-x-0"
                    }`}
                  />
                </button>
              </div>
            </Card>
          ))}
        </div>
      </div>

      <Separator />

      {/* Alert history */}
      <div>
        <h2 className="mb-3 text-sm font-semibold text-ink-3 uppercase tracking-wider">
          Historique des alertes
        </h2>
        <div className="grid gap-3">
          {DEMO_HISTORY.map((item) => (
            <Card
              key={item.id}
              className="border-border/50 bg-white p-4 shadow-sm"
            >
              <div className="flex items-start gap-3">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-amber-50">
                  <AlertTriangle className="h-4 w-4 text-amber-500" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <p className="text-sm font-medium text-ink">
                      {item.alertName}
                    </p>
                    {!item.isRead && (
                      <Badge className="bg-red-100 text-red-700 text-[10px]">
                        Nouveau
                      </Badge>
                    )}
                  </div>
                  <p className="mt-0.5 text-sm text-ink-3">{item.message}</p>
                  <p className="mt-1.5 flex items-center gap-1 text-xs text-ink-3">
                    <Clock className="h-3 w-3" />
                    {new Date(item.triggeredAt).toLocaleDateString("fr-FR", {
                      year: "numeric",
                      month: "long",
                      day: "numeric",
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </p>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
