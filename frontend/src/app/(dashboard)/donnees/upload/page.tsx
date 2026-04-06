"use client";

import { useState } from "react";
import Link from "next/link";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { FileUploadZone } from "@/components/data/file-upload-zone";
import { useUpload } from "@/hooks/use-upload";
import {
  ArrowLeft,
  ArrowRight,
  CheckCircle2,
  FileSpreadsheet,
  Table,
} from "lucide-react";

const DEMO_COLUMNS = [
  { name: "Date", type: "date", sample: "2026-03-15" },
  { name: "Client", type: "string", sample: "Marjane Holding" },
  { name: "Produit", type: "string", sample: "Huile de table 5L" },
  { name: "Categorie", type: "string", sample: "Alimentaire" },
  { name: "Quantite", type: "number", sample: "150" },
  { name: "Prix unitaire", type: "number", sample: "45.00" },
  { name: "Montant total", type: "number", sample: "6750.00" },
  { name: "Ville", type: "string", sample: "Casablanca" },
];

export default function UploadPage() {
  const { progress, isUploading } = useUpload();
  const [step, setStep] = useState<"upload" | "mapping" | "done">("upload");
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);

  function handleFileSelect(file: File) {
    setUploadedFile(file);
    // In production, trigger the real upload here
    // Simulate moving to the mapping step
  }

  function handleContinueToMapping() {
    setStep("mapping");
  }

  function handleFinish() {
    setStep("done");
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6 animate-fade-in">
      <Link
        href="/donnees"
        className="inline-flex items-center text-sm text-ink-3 hover:text-ink transition-colors"
      >
        <ArrowLeft className="mr-1.5 h-4 w-4" />
        Retour aux sources
      </Link>

      <div>
        <h1 className="text-2xl font-bold text-ink tracking-tight">
          Importer des donnees
        </h1>
        <p className="mt-1 text-sm text-ink-3">
          Importez votre fichier Excel ou CSV et mappez les colonnes
        </p>
      </div>

      {/* Step indicator */}
      <div className="flex items-center gap-3">
        {["Fichier", "Colonnes", "Termine"].map((label, i) => (
          <div key={label} className="flex items-center gap-2">
            <div
              className={`flex h-7 w-7 items-center justify-center rounded-full text-xs font-bold ${
                i === 0 && step === "upload"
                  ? "bg-blue-600 text-white"
                  : i === 1 && step === "mapping"
                    ? "bg-blue-600 text-white"
                    : i === 2 && step === "done"
                      ? "bg-blue-600 text-white"
                      : step === "done" || (step === "mapping" && i === 0)
                        ? "bg-emerald-100 text-emerald-700"
                        : "bg-gray-100 text-ink-3"
              }`}
            >
              {(step === "done" && i < 2) ||
              (step === "mapping" && i === 0) ? (
                <CheckCircle2 className="h-4 w-4" />
              ) : (
                i + 1
              )}
            </div>
            <span className="text-xs font-medium text-ink-3">{label}</span>
            {i < 2 && <div className="h-px w-8 bg-gray-200" />}
          </div>
        ))}
      </div>

      {/* Upload step */}
      {step === "upload" && (
        <div className="space-y-4">
          <FileUploadZone
            onFileSelect={handleFileSelect}
            isUploading={isUploading}
            progress={progress}
          />

          {uploadedFile && !isUploading && (
            <div className="flex justify-end">
              <Button
                className="bg-blue-600 hover:bg-blue-700 text-white"
                onClick={handleContinueToMapping}
              >
                Continuer
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </div>
          )}
        </div>
      )}

      {/* Column mapping step */}
      {step === "mapping" && (
        <div className="space-y-4">
          <Card className="border-border/50 bg-white p-5 shadow-sm">
            <div className="flex items-center gap-3 mb-4">
              <Table className="h-5 w-5 text-blue-600" />
              <h3 className="font-semibold text-ink">
                Colonnes detectees ({DEMO_COLUMNS.length})
              </h3>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border">
                    <th className="py-2 pr-4 text-left font-medium text-ink-3">
                      Colonne
                    </th>
                    <th className="py-2 pr-4 text-left font-medium text-ink-3">
                      Type detecte
                    </th>
                    <th className="py-2 pr-4 text-left font-medium text-ink-3">
                      Exemple
                    </th>
                    <th className="py-2 text-left font-medium text-ink-3">
                      Mapper vers
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {DEMO_COLUMNS.map((col) => (
                    <tr key={col.name} className="border-b border-border/50">
                      <td className="py-3 pr-4">
                        <div className="flex items-center gap-2">
                          <FileSpreadsheet className="h-3.5 w-3.5 text-blue-500" />
                          <span className="font-medium text-ink">
                            {col.name}
                          </span>
                        </div>
                      </td>
                      <td className="py-3 pr-4">
                        <span className="inline-flex rounded-full bg-blue-50 px-2 py-0.5 text-xs font-medium text-blue-700">
                          {col.type}
                        </span>
                      </td>
                      <td className="py-3 pr-4 text-ink-3">{col.sample}</td>
                      <td className="py-3">
                        <select className="rounded-md border border-input bg-background px-2 py-1 text-xs">
                          <option>{col.name}</option>
                          <option>Ignorer</option>
                        </select>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>

          <div className="flex justify-between">
            <Button variant="outline" onClick={() => setStep("upload")}>
              <ArrowLeft className="mr-2 h-4 w-4" />
              Retour
            </Button>
            <Button
              className="bg-blue-600 hover:bg-blue-700 text-white"
              onClick={handleFinish}
            >
              Importer les donnees
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </div>
        </div>
      )}

      {/* Done step */}
      {step === "done" && (
        <Card className="border-border/50 bg-white p-10 shadow-sm text-center">
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-emerald-50">
            <CheckCircle2 className="h-8 w-8 text-emerald-600" />
          </div>
          <h3 className="mt-4 text-xl font-bold text-ink">
            Import reussi !
          </h3>
          <p className="mt-2 text-sm text-ink-3">
            {DEMO_COLUMNS.length} colonnes et les donnees ont ete importees.
            L&apos;analyse commencera sous peu.
          </p>
          <div className="mt-6 flex items-center justify-center gap-3">
            <Button variant="outline" render={<Link href="/donnees" />}>
              Voir les sources
            </Button>
            <Button
              className="bg-blue-600 hover:bg-blue-700 text-white"
              render={<Link href="/tableau-de-bord" />}
            >
              Voir le dashboard
            </Button>
          </div>
        </Card>
      )}
    </div>
  );
}
