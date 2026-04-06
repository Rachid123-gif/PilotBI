"use client";

import Link from "next/link";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Database,
  Plus,
  FileSpreadsheet,
  FileText,
  RefreshCw,
  Calendar,
  Rows3,
} from "lucide-react";

const DEMO_DATA_SOURCES = [
  {
    id: "ds1",
    name: "Ventes_Mars_2026.xlsx",
    type: "excel" as const,
    status: "active" as const,
    rowCount: 3_847,
    columnCount: 12,
    lastSyncedAt: "2026-04-01T08:00:00",
  },
  {
    id: "ds2",
    name: "Clients_B2B.csv",
    type: "csv" as const,
    status: "active" as const,
    rowCount: 347,
    columnCount: 8,
    lastSyncedAt: "2026-03-28T14:30:00",
  },
  {
    id: "ds3",
    name: "Stock_Inventaire.xlsx",
    type: "excel" as const,
    status: "processing" as const,
    rowCount: 1_256,
    columnCount: 15,
    lastSyncedAt: null,
  },
];

const TYPE_ICONS = {
  excel: FileSpreadsheet,
  csv: FileText,
  google_sheets: FileSpreadsheet,
  odoo: Database,
  sage: Database,
};

const STATUS_CONFIG = {
  active: {
    label: "Actif",
    className: "bg-emerald-50 text-emerald-700 border-emerald-200",
  },
  processing: {
    label: "Traitement",
    className: "bg-amber-50 text-amber-700 border-amber-200",
  },
  pending: {
    label: "En attente",
    className: "bg-gray-50 text-ink-3 border-gray-200",
  },
  error: {
    label: "Erreur",
    className: "bg-red-50 text-red-700 border-red-200",
  },
};

export default function DonneesPage() {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-ink tracking-tight">
            Sources de donnees
          </h1>
          <p className="mt-1 text-sm text-ink-3">
            Gerez vos sources de donnees connectees
          </p>
        </div>
        <Button
          className="bg-blue-600 hover:bg-blue-700 text-white"
          render={<Link href="/donnees/upload" />}
        >
          <Plus className="mr-2 h-4 w-4" />
          Ajouter une source
        </Button>
      </div>

      <div className="grid gap-4">
        {DEMO_DATA_SOURCES.map((source) => {
          const Icon = TYPE_ICONS[source.type];
          const status = STATUS_CONFIG[source.status];

          return (
            <Card
              key={source.id}
              className="border-border/50 bg-white p-5 shadow-sm hover:shadow-md transition-all duration-200"
            >
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div className="flex items-center gap-4">
                  <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-50">
                    <Icon className="h-6 w-6 text-blue-600" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2 flex-wrap">
                      <h3 className="font-semibold text-ink">{source.name}</h3>
                      <Badge variant="outline" className={status.className}>
                        {status.label}
                      </Badge>
                    </div>
                    <div className="mt-1 flex items-center gap-4 text-xs text-ink-3">
                      <span className="flex items-center gap-1">
                        <Rows3 className="h-3 w-3" />
                        {source.rowCount.toLocaleString("fr-FR")} lignes
                      </span>
                      <span>{source.columnCount} colonnes</span>
                      {source.lastSyncedAt && (
                        <span className="flex items-center gap-1">
                          <Calendar className="h-3 w-3" />
                          {new Date(source.lastSyncedAt).toLocaleDateString(
                            "fr-FR"
                          )}
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                <Button variant="outline" size="sm">
                  <RefreshCw className="mr-1.5 h-3.5 w-3.5" />
                  Synchroniser
                </Button>
              </div>
            </Card>
          );
        })}
      </div>

      {/* Empty state for when no sources */}
      {DEMO_DATA_SOURCES.length === 0 && (
        <Card className="flex flex-col items-center justify-center border-dashed border-2 border-border bg-gray-50/50 p-12 text-center">
          <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-50">
            <Database className="h-8 w-8 text-blue-600" />
          </div>
          <h3 className="mt-4 text-lg font-semibold text-ink">
            Aucune source de donnees
          </h3>
          <p className="mt-1 text-sm text-ink-3 max-w-sm">
            Importez vos fichiers Excel ou CSV pour commencer a analyser vos
            donnees
          </p>
          <Button
            className="mt-6 bg-blue-600 hover:bg-blue-700 text-white"
            render={<Link href="/donnees/upload" />}
          >
            <Plus className="mr-2 h-4 w-4" />
            Importer des donnees
          </Button>
        </Card>
      )}
    </div>
  );
}
