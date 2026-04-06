"use client";

import { useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { ArrowRight, ArrowLeft, Upload, FileCheck, X } from "lucide-react";
import { cn } from "@/lib/utils";

export default function OnboardingStep4() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [isDragOver, setIsDragOver] = useState(false);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && isValidFile(droppedFile)) {
      setFile(droppedFile);
    }
  }, []);

  const handleFileInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const selectedFile = e.target.files?.[0];
      if (selectedFile && isValidFile(selectedFile)) {
        setFile(selectedFile);
      }
    },
    []
  );

  function isValidFile(f: File): boolean {
    const validTypes = [
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      "application/vnd.ms-excel",
      "text/csv",
    ];
    return validTypes.includes(f.type) || f.name.endsWith(".csv") || f.name.endsWith(".xlsx");
  }

  function formatFileSize(bytes: number): string {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / (1024 * 1024)).toFixed(1) + " MB";
  }

  function handleNext() {
    // In a real app, upload the file here
    const prev = JSON.parse(sessionStorage.getItem("onboarding") || "{}");
    sessionStorage.setItem(
      "onboarding",
      JSON.stringify({ ...prev, hasFile: !!file, fileName: file?.name })
    );
    router.push("/onboarding/confirmation");
  }

  function handleSkip() {
    router.push("/onboarding/confirmation");
  }

  return (
    <div className="animate-fade-in">
      <div className="mb-8 text-center">
        <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-50">
          <Upload className="h-7 w-7 text-blue-600" />
        </div>
        <h1 className="text-2xl font-bold text-ink">
          Importez vos donnees
        </h1>
        <p className="mt-2 text-sm text-ink-3">
          Glissez-deposez votre fichier Excel ou CSV
        </p>
      </div>

      {!file ? (
        <div
          onDragOver={(e) => {
            e.preventDefault();
            setIsDragOver(true);
          }}
          onDragLeave={() => setIsDragOver(false)}
          onDrop={handleDrop}
          className={cn(
            "flex flex-col items-center gap-4 rounded-2xl border-2 border-dashed p-10 text-center transition-all duration-200",
            isDragOver
              ? "border-blue-500 bg-blue-50"
              : "border-gray-200 bg-gray-50/50 hover:border-blue-300 hover:bg-blue-50/30"
          )}
        >
          <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-100">
            <Upload className="h-8 w-8 text-blue-600" />
          </div>
          <div>
            <p className="text-sm font-medium text-ink">
              Glissez votre fichier ici
            </p>
            <p className="mt-1 text-xs text-ink-3">
              ou cliquez pour selectionner
            </p>
          </div>
          <label className="cursor-pointer">
            <span className="inline-flex items-center rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 transition-colors">
              Parcourir
            </span>
            <input
              type="file"
              accept=".xlsx,.csv"
              onChange={handleFileInput}
              className="hidden"
            />
          </label>
          <p className="text-xs text-ink-3">
            Formats acceptes : .xlsx, .csv (max. 10 MB)
          </p>
        </div>
      ) : (
        <div className="rounded-2xl border border-green-200 bg-green-50 p-6">
          <div className="flex items-start gap-4">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-green-100">
              <FileCheck className="h-6 w-6 text-green-600" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="font-medium text-green-800 truncate">
                {file.name}
              </p>
              <p className="text-sm text-green-600">
                {formatFileSize(file.size)}
              </p>
            </div>
            <button
              type="button"
              onClick={() => setFile(null)}
              className="rounded-lg p-1.5 text-green-600 hover:bg-green-100 transition-colors"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}

      <div className="mt-8 flex gap-3">
        <Button
          variant="outline"
          className="flex-1 h-11"
          onClick={() => router.push("/onboarding/donnees")}
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Retour
        </Button>
        <Button
          className="flex-1 bg-blue-600 hover:bg-blue-700 text-white h-11"
          onClick={handleNext}
        >
          {file ? "Continuer" : "Passer"}
          <ArrowRight className="ml-2 h-4 w-4" />
        </Button>
      </div>

      {!file && (
        <button
          type="button"
          onClick={handleSkip}
          className="mt-4 w-full text-center text-sm text-ink-3 hover:text-blue-600 transition-colors"
        >
          Je le ferai plus tard
        </button>
      )}
    </div>
  );
}
